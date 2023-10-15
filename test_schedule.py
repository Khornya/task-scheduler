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
        "start": [2],
        "end": [5],
        "tags": [['Perso']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] >= 2
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
    assert result["tasks"][1]["isPresent"] == False


def test_schedule_event_should_plan_in_reserved_interval_even_if_one_tag_does_not_match_case_reserved_tag():
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
        "start": [2],
        "end": [5],
        "tags": [['Perso', 'Autre']]
    }, dtype=object)
    start = 0
    result = schedule(tasks, reserved_intervals, reserved_tags, start)
    assert result["found"] == True
    assert result["tasks"][1]["start"] >= 2


def test_schedule_event_should_plan_events():
    tasks = pd.DataFrame({
        "id": ['2a6laipv4ttscfdo4kn6vj6hcv', 'c4rj4c33c4qjebb160q38b9k6gq3cb9o6sq68b9gcko66dr2c8ojgob6c4'],
        "impact": [10, 60],
        "duration": [2, 12],
        "dueDate": [5661192, 5658000],
        "maxDueDate": [5679924, 5658288],
        "tags": [['Ouvré'], []]
    }, dtype=object)
    reserved_tags = pd.DataFrame({
        "id": ['0', '121'],
        "start": [5657544, 5658120],
        "end": [5657664, 5658252],
        "tags": [['Ouvré'], ['Ouvré']]
    }, dtype=object)
    reserved_intervals = pd.DataFrame({
        "id": ['64o6cd1j6gr6abb46ks66b9k69ij2bb174rm4bb2c5i6cc1lcgr64phl6s'],
        "start": [5675556],
        "end": [5675568]
    }, dtype=object)
    result = schedule(tasks, reserved_intervals, reserved_tags, 5657816)
    assert result["found"] == True
    assert result["tasks"]['2a6laipv4ttscfdo4kn6vj6hcv']["isPresent"] == True
    assert result["tasks"]['2a6laipv4ttscfdo4kn6vj6hcv']["start"] >= 5658120
    assert result["tasks"]['2a6laipv4ttscfdo4kn6vj6hcv']["end"] <= 5658252
    assert result["tasks"]['c4rj4c33c4qjebb160q38b9k6gq3cb9o6sq68b9gcko66dr2c8ojgob6c4']["isPresent"] == True
    assert result["tasks"]['c4rj4c33c4qjebb160q38b9k6gq3cb9o6sq68b9gcko66dr2c8ojgob6c4']["end"] < 5658120