import subprocess
import sys
from datetime import datetime



def run_module(module):

    print()
    print("=" * 60)
    print(
        "RUNNING:",
        module
    )
    print("=" * 60)


    result = subprocess.run(
        [
            sys.executable,
            "-m",
            module
        ]
    )


    if result.returncode != 0:

        print(
            "FAILED:",
            module
        )

        return False


    print(
        "COMPLETE:",
        module
    )

    return True




def run_pipeline():


    print()
    print("=" * 60)
    print("AI TRADING DAILY PIPELINE")
    print(
        datetime.now()
    )
    print("=" * 60)



    modules = [

        "app.market_scanner",

        "app.integrated_scanner",

        "app.ai_decision",

        "app.trade_history_manager",

        "app.live_trade_monitor",

        "app.trade_feedback",

        "app.ai_learning_engine",

        "app.ai_report"

    ]



    for module in modules:

        success = run_module(
            module
        )


        if not success:

            print(
                "Pipeline stopped."
            )

            return



    print()

    print("=" * 60)
    print("AI PIPELINE COMPLETE")
    print("=" * 60)




if __name__ == "__main__":

    run_pipeline()