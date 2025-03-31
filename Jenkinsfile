pipeline {
    agent any
    environment {
        // Environment variable to flag whether drift was detected
        DRIFT_DETECTED = "false"
    }
    stages {
        stage('Drift Detection') {
            steps {
                script {
                    // Run the drift detector script and capture its output.
                    def driftOutput = sh(script: "python3 monitoring/drift_detector.py", returnStdout: true).trim()
                    echo "Drift Detector Output:\n${driftOutput}"
                    
                    // Check if the output contains "[ALERT]".
                    if (driftOutput.contains("[ALERT]")) {
                        echo "Drift detected! Setting DRIFT_DETECTED to true."
                        env.DRIFT_DETECTED = "true"
                    } else {
                        echo "No significant drift detected."
                    }
                }
            }
        }
        stage('Retrain Model') {
            when {
                // Only execute this stage if drift was detected.
                expression { env.DRIFT_DETECTED == "true" }
            }
            steps {
                echo "Drift detected. Starting model retraining..."
                // Run the training script to update the model and baseline training stats.
                sh "python3 retraining/train_model.py"
            }
        }
    }
    post {
        always {
            echo "Pipeline execution completed."
        }
    }
}