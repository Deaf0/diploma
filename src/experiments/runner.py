from logging import config
import time
import random
import numpy as np
from pathlib import Path

from src.sampling.config import SamplingConfig
from src.experiments.common import compute_ground_truth
from src.experiments.experiment_fixed_shift import run_single_case_exp1
from src.experiments.experiment_optimize_shift import run_single_case_exp2
from src.experiments.save_result import ResultCSVWriter
from src.experiments.test_data import get_pair_polygons
from src.experiments.utils import enrich_result, build_error_message, stable_seed


# config

BASE_PATH = Path(__file__).parents[2] / "data" 
N_VALUES = [25, 100, 400, 450, 500, 550, 600,  700,  800]
METHODS = ["raster", "fps", "n_net"]
NUM_CASES = 35
SEED = 42
REPEATS = 3

dataset_rng = random.Random(SEED)
np_rng = np.random.default_rng(SEED)

Path("results/results_exp1.csv").unlink(missing_ok=True)
Path("results/results_exp2.csv").unlink(missing_ok=True)

exp1_writer = ResultCSVWriter(
    "results/results_exp1.csv",
    fieldnames=[
        "experiment",
        "method",
        "total_points",
        "H_reference",
        "H_est",
        "signed_H_err",
        "abs_H_err",
        "A_name",
        "B_name",
        "case",
        "repeat_id",
        "time"
    ]
)

exp2_writer = ResultCSVWriter(
    "results/results_exp2.csv",
    fieldnames=[
        "experiment",
        "method",
        "total_points",
        "H_reference",
        "H_est",
        "x_err",
        "signed_H_err",
        "abs_H_err",
        "A_name",
        "B_name",
        "case",
        "repeat_id",
        "time"
    ]
)

failure_writer = ResultCSVWriter(
    "results/failures.csv",
    fieldnames=[
        "case",
        "method",
        "total_points",
        "experiment",
        "error_message"
    ]
)

for case_id in range(NUM_CASES):
    print(f"\n[CASE {case_id}]")

    case_data = get_pair_polygons(BASE_PATH, dataset_rng)
    A = case_data["A"]
    B = case_data["B"]

    ground_truth_config = SamplingConfig(
        method="raster", 
        total_points=10000, 
        rng=random.Random(SEED + case_id)      
    )

    try:
        x_reference, H_reference, A_dense, B_dense, Q0 = compute_ground_truth(A, B, ground_truth_config) 
    except Exception as e:
        error_message = build_error_message(
                            "[GROUND_TRUTH FAILED]",
                            case_id,
                            "no method",
                            ground_truth_config.total_points,
                            e
                        )
        print(error_message)
        
        failure_writer.write(error_message)
        continue

    for method in METHODS:
        for n in N_VALUES:
            for repeat_id in range(REPEATS):
                exp1_seed = stable_seed(case_id, method, n, repeat_id, "exp1")
                exp2_seed = stable_seed(case_id, method, n, repeat_id, "exp2")

                exp1_config = SamplingConfig(
                    method=method, 
                    total_points=n, 
                    rng=random.Random(exp1_seed)
                )
                exp2_config = SamplingConfig(
                    method=method, 
                    total_points=n, 
                    rng=random.Random(exp2_seed)
                )

                print(f"  method={method}, n={n}")

                #First experiment
                try:
                    start = time.time()

                    first_result = run_single_case_exp1(
                        A=A,
                        B=B,
                        config=exp1_config,
                        x_reference=x_reference,
                        H_reference=H_reference
                    )

                    first_result = enrich_result(
                        first_result,
                        case_data,
                        case_id,
                        repeat_id,
                        time.time() - start
                    )

                    exp1_writer.write(first_result)

                except Exception as e:
                    error_message = build_error_message(
                        "[EXP1 FAILED]",
                        case_id,
                        method,
                        n,
                        e
                    )
                    print(error_message)
                    failure_writer.write(error_message)

                #Second experiment
                try:
                    start = time.time()

                    second_result = run_single_case_exp2(
                        A=A,
                        B=B,
                        config=exp2_config,
                        Q0=Q0,
                        A_dense=A_dense,
                        B_dense=B_dense,
                        x_reference=x_reference,
                        H_reference=H_reference
                    )

                    second_result = enrich_result(
                        second_result,
                        case_data,
                        case_id,
                        repeat_id,
                        time.time() - start
                    )

                    exp2_writer.write(second_result)

                except Exception as e:
                    error_message = build_error_message(
                        "[EXP2 FAILED]",
                        case_id,
                        method,
                        n,
                        e
                    )
                    print(error_message)
                    failure_writer.write(error_message)

exp1_writer.close()
exp2_writer.close()
failure_writer.close()