pipeline {
    agent any

    stages {
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
                    // Write the result to a file so that the next stage can read it.
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
                        // Execute the training script to retrain the model.
                        sh "python3 retraining/train_model.py"
                    } else {
                        echo "No drift detected. Skipping retraining."
                    }
                }
            }
        }
    }
    post {
        always {
            echo "Pipeline execution completed."
        }
    }
}