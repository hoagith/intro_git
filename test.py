import pandas as pd

# CSV読込
# file_path = "冷蔵庫クーリングアシスト連続利用_2026-08-27-1450_1.csv"
file_path = "mudai.csv"
df = pd.read_csv(file_path)

# 日時変換
df["LDC_TIMESTAMP"] = pd.to_datetime(df["LDC_TIMESTAMP"])

# モード列名
mode_col = "c_mode"

results = []

for i in range(len(df) - 1):
    curr_time = df.loc[i, "LDC_TIMESTAMP"]
    next_time = df.loc[i + 1, "LDC_TIMESTAMP"]

    curr_mode = df.loc[i, mode_col]
    next_mode = df.loc[i + 1, mode_col]

    time_diff = next_time - curr_time

    if (
        time_diff <= pd.Timedelta(minutes=5)
        and curr_mode == 0
        and next_mode != 0
    ):
        results.append({
            "No": len(results) + 1,
            "zengyojikoku": curr_time,
            "senijikoku": next_time,
            "jikansa_s": int(time_diff.total_seconds()),
            "modeti": next_mode
        })

# 結果DataFrame
result_df = pd.DataFrame(results)

print("gaitokensu:", len(result_df))
print(result_df)

# CSV出力
result_df.to_csv(
    "CA.csv",
    index=False,
    encoding="utf-8-sig"
)

# モード別集計
if len(result_df) > 0:
    print("\nmodebetsukensu")
    print(result_df["modeti"].value_counts().sort_index())