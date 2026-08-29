import os
import subprocess


class VisionService:

    @staticmethod
    def reconocer_mano():

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        mano_path = os.path.join(
            base_dir,
            "vision",
            "mano.py"
        )

        if not os.path.exists(mano_path):
            raise FileNotFoundError(
                f"No se encontró el archivo: {mano_path}"
            )

        subprocess.Popen(
            ["python", mano_path],
            cwd=base_dir
        )

        return True