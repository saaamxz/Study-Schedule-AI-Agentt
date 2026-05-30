import pandas as pd

schedule_df = pd.read_csv("my_schedule_AI_sec4.csv")
lectures_df = pd.read_csv("schedule.csv")
exams_df = pd.read_csv("exams.csv")
def get_schedule(day):
    day = day.strip()

    rows = schedule_df[schedule_df["day"] == day]

    if rows.empty:
        return "No schedule found"

    return rows.to_string(index=False)


def get_subject_info(subject):
    subject = subject.strip()

    rows = schedule_df[
        schedule_df["subject"].str.contains(subject, case=False, na=False)
    ]

    if rows.empty:
        return "No subject data"

    return rows.to_string(index=False)



def get_lectures(subject):
    subject = subject.strip()

    rows = lectures_df[
        lectures_df["subject"].str.contains(subject, case=False, na=False)
    ]

    if rows.empty:
        return "No lectures found"

    return rows.to_string(index=False)

# GET EXAMS

def get_exam_schedule(subject):
    subject = subject.strip()

    rows = exams_df[
        exams_df["subject"].str.contains(subject, case=False, na=False)
    ]

    if rows.empty:
        return "No exams found"

    return rows.to_string(index=False)


def get_day_plan(day):
    day = day.strip()

    schedule_rows = schedule_df[schedule_df["day"] == day]
    lecture_rows = lectures_df[lectures_df["day"] == day]

    result = f"""
=== SCHEDULE ===
{schedule_rows.to_string(index=False) if not schedule_rows.empty else "No schedule"}

=== LECTURES ===
{lecture_rows.to_string(index=False) if not lecture_rows.empty else "No lectures"}
"""

    return result

def smart_search(query):
    query = query.lower()

    results = []

    for df_name, df in {
        "Schedule": schedule_df,
        "Lectures": lectures_df,
        "Exams": exams_df
    }.items():

        for _, row in df.iterrows():

            row_text = " ".join([str(x) for x in row.values]).lower()

            score = sum(
                1 for word in query.split()
                if word in row_text
            )

            if score > 0:
                results.append(
                    f"[{df_name}] {row.to_dict()}"
                )

    if not results:
        return "No data found"

    return "\n\n".join(results[:10])