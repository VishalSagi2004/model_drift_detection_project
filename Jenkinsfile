pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                echo "Installing Python dependencies from requirements.txt..."
                // Use python3 -m pip to install dependencies (pip3)
                sh 'python3 -m pip install -r requirements.txt'
            }
        }
        stage('Drift Detection') {
            steps {
                script {
                    // Run the drift detector and capture its output.
                    def driftOutput = sh(script: "python3 monitoring/drift_detector.py", returnStdout: true).trim()
                    echo "Drift Detector Output:\n${driftOutput}"
                    
                    // Determine if drift was detected.
                    def driftDetected = "false"
                    if (driftOutput.contains("[ALERT]")) {
                        echo "Drift detected! Setting driftDetected to true."
                        driftDetected = "true"
                    } else {
                        echo "No significant drift detected."
                    }
                    // Write the result to a file for use in the next stage.
                    writeFile file: 'drift_result.txt', text: driftDetected
                }
            }
        }
        stage('Retrain Model') {
            steps {
                script {
                    // Read the drift detection result from the file.
                    def result = readFile('drift_result.txt').trim()
                    if (result == "true") {
                        echo "Drift detected. Starting model retraining..."
                        // Run the training script to retrain the model and update baseline stats.
                        sh "python3 retraining/train_model.py"
                    } else {
                        echo "No drift detected. Skipping retraining."
                    }
                }
            }
        }
        stage('Post-Retrain Verification') {
            steps {
                echo "Verifying updated model and training stats..."
                // List file details for the model file and training stats.
                sh "ls -l model/model_v1.pkl"
                sh "ls -l monitoring/training_stats.json"
            }
        }
    }
    post {
        always {
            echo "Pipeline execution completed."
        }
    }
}