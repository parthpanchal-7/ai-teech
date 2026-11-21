"""Small teacher-reviewable Electricity syllabus and questions for the MVP."""

CONCEPTS = [
    {"id":"current","title":"Electric Current","prerequisites":[],"description":"Rate of flow of charge; I = Q/t."},
    {"id":"potential","title":"Potential Difference","prerequisites":["current"],"description":"Work done per unit charge; V = W/Q."},
    {"id":"resistance","title":"Resistance","prerequisites":["current","potential"],"description":"Opposition to current and its dependence on conductor properties."},
    {"id":"ohms_law","title":"Ohm's Law","prerequisites":["potential","resistance"],"description":"For a suitable conductor at constant temperature, V = IR."},
    {"id":"series","title":"Series Circuits","prerequisites":["ohms_law"],"description":"Same current flows through series resistors; resistances add."},
    {"id":"parallel","title":"Parallel Circuits","prerequisites":["ohms_law"],"description":"Parallel branches share voltage; branch currents add."},
    {"id":"power","title":"Electric Power","prerequisites":["ohms_law"],"description":"Power is energy transferred per second; P = VI."},
]

QUESTIONS = [
    {"id":"q1","concept_id":"current","difficulty":"easy","prompt":"If 10 coulombs of charge pass in 2 seconds, what is the current?","options":["5 A","20 A","12 A","0.2 A"],"answer":0,"explanation":"Current I = Q/t = 10/2 = 5 A.","keywords":["charge","time","divide"]},
    {"id":"q2","concept_id":"potential","difficulty":"easy","prompt":"What does potential difference measure?","options":["Work per unit charge","Charge per second","Opposition to current","Energy per second"],"answer":0,"explanation":"Potential difference is work done per unit charge.","keywords":["work","charge","energy"]},
    {"id":"q3","concept_id":"resistance","difficulty":"easy","prompt":"At fixed voltage, increasing resistance makes current...","options":["Increase","Decrease","Stay equal","Become zero always"],"answer":1,"explanation":"By Ohm's law I = V/R, so increasing R decreases I at constant V.","keywords":["oppose","decrease","inverse","voltage"]},
    {"id":"q4","concept_id":"ohms_law","difficulty":"easy","prompt":"At constant voltage, if resistance doubles, current becomes...","options":["Double","Half","Four times","Unchanged"],"answer":1,"explanation":"I = V/R, so doubling R halves current when V is constant.","keywords":["inverse","half","divide","constant"]},
    {"id":"q5","concept_id":"ohms_law","difficulty":"medium","prompt":"A 12 V battery is connected to a 4 ohm resistor. Find current.","options":["48 A","3 A","8 A","0.33 A"],"answer":1,"explanation":"I = V/R = 12/4 = 3 A.","keywords":["divide","voltage","resistance","ohm"]},
    {"id":"q6","concept_id":"ohms_law","difficulty":"hard","prompt":"At fixed 10 V, a 5 ohm resistor is replaced by a 10 ohm resistor. Compare current.","options":["2 A to 1 A","1 A to 2 A","5 A to 10 A","Both 2 A"],"answer":0,"explanation":"I = 10/5 = 2 A initially, then 10/10 = 1 A.","keywords":["inverse","divide","half","voltage"]},
    {"id":"q7","concept_id":"series","difficulty":"easy","prompt":"In a series circuit, which quantity is equal through all resistors?","options":["Voltage","Current","Resistance","Power"],"answer":1,"explanation":"Series elements carry the same current.","keywords":["same","current","one path"]},
    {"id":"q8","concept_id":"series","difficulty":"medium","prompt":"Two resistors of 2 ohms and 3 ohms are in series. Equivalent resistance?","options":["1.2 ohms","5 ohms","6 ohms","0.5 ohms"],"answer":1,"explanation":"Series resistances add: 2 + 3 = 5 ohms.","keywords":["add","sum","series"]},
    {"id":"q9","concept_id":"parallel","difficulty":"easy","prompt":"In parallel branches, which quantity is common?","options":["Current","Voltage","Resistance","Power"],"answer":1,"explanation":"Each branch is connected across the same two nodes, so voltage is equal.","keywords":["same","voltage","branches"]},
    {"id":"q10","concept_id":"parallel","difficulty":"medium","prompt":"Two 6-ohm resistors are in parallel. Equivalent resistance?","options":["12 ohms","6 ohms","3 ohms","1 ohm"],"answer":2,"explanation":"1/R = 1/6 + 1/6, so R = 3 ohms.","keywords":["reciprocal","half","parallel"]},
    {"id":"q11","concept_id":"power","difficulty":"easy","prompt":"Which expression calculates electric power?","options":["P = V/I","P = VI","P = IR","P = Q/t"],"answer":1,"explanation":"Power P = voltage times current = VI.","keywords":["voltage","current","multiply"]},
    {"id":"q12","concept_id":"power","difficulty":"medium","prompt":"A 10 V device draws 2 A. What is its power?","options":["5 W","12 W","20 W","0.2 W"],"answer":2,"explanation":"P = VI = 10 x 2 = 20 W.","keywords":["multiply","voltage","current"]},
]

QUESTION_BY_ID = {question["id"]: question for question in QUESTIONS}
CONCEPT_BY_ID = {concept["id"]: concept for concept in CONCEPTS}

def public_question(question):
    """Answer key is intentionally withheld from student-facing question payloads."""
    return {key: question[key] for key in ("id","concept_id","difficulty","prompt","options")}
