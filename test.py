from schedule_ortools import schedule
import pandas as pd


def test_schedule_event_should_schedule_all_events_if_possible_case_same_due_dates():
    tasks = pd.DataFrame({
        "id": [1,2,3,4,5],
        "impact": [2,3,6,4,1],
        "duration": [4,2,5,2,2],
        "dueDate": [10,10,10,10,10],
        "maxDueDate": [15,15,15,15,15],
        "tags": [[],[],[],[],[]]
    })
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame([])
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["found"] == True
    assert result["tasks"][1]["isPresent"] == True
    assert result["tasks"][2]["isPresent"] == True
    assert result["tasks"][3]["isPresent"] == True
    assert result["tasks"][4]["isPresent"] == True
    assert result["tasks"][5]["isPresent"] == True


def test_schedule_event_should_schedule_all_events_if_possible_case_different_due_dates():
    tasks = pd.DataFrame({
        "id": [1,2,3,4,5],
        "impact": [2,3,6,4,1],
        "duration": [4,2,5,2,2],
        "dueDate": [2,5,8,12,14],
        "maxDueDate": [4,6,11,13,15],
        "tags": [[],[],[],[],[]]
    })
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame([])
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["isPresent"] == True
    assert result["tasks"][2]["isPresent"] == True
    assert result["tasks"][3]["isPresent"] == True
    assert result["tasks"][4]["isPresent"] == True
    assert result["tasks"][5]["isPresent"] == True


def test_schedule_event_should_start_as_soon_as_possible():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [[]]
    })
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame([])
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    print(result)
    assert result["found"] == True
    assert result["tasks"][1]["isLate"] == False
    assert result["tasks"][1]["start"] == 0


def test_schedule_event_should_avoid_reserved_intervals():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [[]]
    }, dtype=object)
    reserved_intervals = pd.DataFrame({
        "start": [0],
        "end": [5]
    }, dtype=object)
    reserved_tags = pd.DataFrame([])
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] >= 5


def test_schedule_event_should_avoid_reserved_tags():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [[]]
    }, dtype=object)
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame({
        "start": [0],
        "end": [5],
        "tags": [['Unavailable']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] >= 5


def test_schedule_event_should_plan_in_reserved_interval_if_one_tag_matches():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [['Perso']]
    }, dtype=object)
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame({
        "start": [0],
        "end": [5],
        "tags": [['Perso']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] < 5


def test_schedule_event_should_plan_events_with_best_impact_per_hour_first():
    tasks = pd.DataFrame({
        "id": [1,2,3,4,5,6],
        "impact": [3,3,6,4,1,5],
        "duration": [4,2,5,2,2,6],
        "dueDate": [2,5,8,12,14,15],
        "maxDueDate": [4,6,11,13,15,20],
        "tags": [[],[],[],[],[],[]]
    })
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame([])
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["isPresent"] == True
    assert result["tasks"][2]["isPresent"] == True
    assert result["tasks"][3]["isPresent"] == True
    assert result["tasks"][4]["isPresent"] == True
    assert result["tasks"][5]["isPresent"] == False
    assert result["tasks"][6]["isPresent"] == True


def test_schedule_event_should_not_plan_in_reserved_interval_if_one_tag_does_not_match_case_task_tag():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [['Perso','Autre']]
    }, dtype=object)
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame({
        "start": [0],
        "end": [5],
        "tags": [['Perso']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] >= 5


def test_schedule_event_should_plan_in_reserved_interval_event_if_one_tag_does_not_match_case_reserved_tag():
    tasks = pd.DataFrame({
        "id": [1],
        "impact": [2],
        "duration": [3],
        "dueDate": [10],
        "maxDueDate": [15],
        "tags": [['Perso']]
    }, dtype=object)
    reserved_intervals = pd.DataFrame([])
    reserved_tags = pd.DataFrame({
        "start": [0],
        "end": [5],
        "tags": [['Perso', 'Autre']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] == 0