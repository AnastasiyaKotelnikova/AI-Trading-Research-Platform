import os
import subprocess
import datetime
import sys
import logging
import json


# --------------------------------------------------
# Create directories
# --------------------------------------------------

os.makedirs(
    "data/logs",
    exist_ok=True
)


# --------------------------------------------------
# Configure logging
# --------------------------------------------------

logging.basicConfig(
    filename="data/logs/daily_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# --------------------------------------------------
# Pipeline status tracking
# --------------------------------------------------

STATUS_FILE = (
    "data/logs/pipeline_status.json"
)


def update_pipeline_status(
    status,
    current_step=None,
    completed_steps=None,
    failed_step=None,
    start_time=None,
    end_time=None,
    duration=None
):

    data = {

        "pipeline_status": status,

        "current_step": current_step,

        "completed_steps": completed_steps or [],

        "failed_step": failed_step,

        "start_time":
            str(start_time)
            if start_time else None,

        "end_time":
            str(end_time)
            if end_time else None,

        "duration":
            str(duration)
            if duration else None,

        "last_updated":
            str(datetime.datetime.now())

    }


    with open(
        STATUS_FILE,
        "w"
    ) as f:

        json.dump(
            data,
            f,
            indent=4
        )



# --------------------------------------------------
# Pipeline modules
# --------------------------------------------------

PIPELINE_STEPS = [

    (
        "Running Integrated Scanner",
        "app.integrated_scanner"
    ),

    (
        "Saving Signal History",
        "app.signal_tracker"
    ),

    (
        "Running Forward Test",
        "app.forward_test"
    ),

    (
        "Updating Trade Database",
        "app.trade_database"
    ),

    (
        "Generating AI Rankings",
        "app.ai_signal_engine"
    ),

    (
        "Generating AI Decisions",
        "app.ai_decision"
    ),

    (
        "Generating AI Report",
        "app.ai_report"
    ),

    (
        "Updating Model Feedback Loop",
        "app.model_feedback_loop"
    ),

    (
        "Updating Model Champion Tracker",
        "app.model_champion_tracker"
    )

]



# --------------------------------------------------
# Run individual pipeline step
# --------------------------------------------------

def run_step(description, module):


    print("\n")
    print("=" * 60)
    print(description)
    print("=" * 60)


    logging.info(
        f"STARTING: {description}"
    )


    result = subprocess.run(

        [
            sys.executable,
            "-m",
            module
        ],

        cwd="C:\\Users\\anast\\scanner-project",

        capture_output=True,

        text=True,

        encoding="utf-8",

        errors="replace"

    )


    if result.stdout:

        print(result.stdout)



    if result.returncode != 0:


        print(
            "FAILED:",
            description
        )


        print("\nERROR DETAILS:")


        if result.stderr:

            print(result.stderr)


        if result.stdout:

            print(result.stdout)



        logging.error(
            f"FAILED: {description}"
        )


        logging.error(
            result.stderr
        )


        logging.error(
            result.stdout
        )


        return False



    print(
        "COMPLETED:",
        description
    )


    logging.info(
        f"COMPLETED: {description}"
    )


    return True




# --------------------------------------------------
# Main pipeline controller
# --------------------------------------------------

def run_pipeline():


    start_time = datetime.datetime.now()


    completed_steps = []



    update_pipeline_status(

        "RUNNING",

        start_time=start_time

    )



    logging.info("=" * 60)

    logging.info(
        "AI STOCK SCANNER PIPELINE STARTED"
    )

    logging.info("=" * 60)



    print("\n")

    print("=" * 60)

    print(
        "AI STOCK SCANNER PIPELINE STARTED"
    )

    print("=" * 60)


    print(start_time)



    # ----------------------------------------------
    # Execute pipeline
    # ----------------------------------------------

    for name, module in PIPELINE_STEPS:



        update_pipeline_status(

            "RUNNING",

            current_step=name,

            completed_steps=completed_steps,

            start_time=start_time

        )



        success = run_step(

            name,

            module

        )



        if not success:


            end_time = datetime.datetime.now()


            duration = (
                end_time - start_time
            )



            update_pipeline_status(

                "FAILED",

                current_step=name,

                completed_steps=completed_steps,

                failed_step=name,

                start_time=start_time,

                end_time=end_time,

                duration=duration

            )



            logging.error(
                "PIPELINE STOPPED"
            )


            print(
                "\nPipeline stopped."
            )


            return



        completed_steps.append(name)



        update_pipeline_status(

            "RUNNING",

            completed_steps=completed_steps,

            start_time=start_time

        )



    # ----------------------------------------------
    # Pipeline completed
    # ----------------------------------------------


    end_time = datetime.datetime.now()


    duration = (
        end_time - start_time
    )



    update_pipeline_status(

        "COMPLETED",

        completed_steps=completed_steps,

        start_time=start_time,

        end_time=end_time,

        duration=duration

    )



    print("\n")

    print("=" * 60)

    print(
        "PIPELINE COMPLETE"
    )

    print("=" * 60)


    print(end_time)



    logging.info("=" * 60)

    logging.info(
        "PIPELINE COMPLETE"
    )


    logging.info(
        end_time
    )


    logging.info(
        f"Duration: {duration}"
    )


    logging.info("=" * 60)




# --------------------------------------------------
# Program entry point
# --------------------------------------------------

if __name__ == "__main__":

    run_pipeline()
