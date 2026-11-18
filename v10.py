import os
import json
import random

PROGRESS_FILE = "v10_progress.json"

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "attempted": 0,
            "correct": 0,
            "wrong": [],
            "topic_scores": {}
        }

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_progress():
    data = load_progress()

    print("\n===== V10 LEARNING PROGRESS =====")
    print("Total Attempted:", data["attempted"])
    print("Correct Answers:", data["correct"])

    if data["attempted"] > 0:
        accuracy = data["correct"] / data["attempted"] * 100
        print("Accuracy:", round(accuracy, 1), "%")

    print("Wrong Questions:", len(data["wrong"]))

    print("\nTopic-wise Scores:")
    for topic, score in data["topic_scores"].items():
        print(topic, ":", score)
import os
import json
import random

PROGRESS_FILE = "v10_progress.json"

def load_progress():
    try:
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "attempted": 0,
            "correct": 0,
            "wrong": [],
            "topic_scores": {}
        }

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def show_progress():
    data = load_progress()

    print("\n===== V10 LEARNING PROGRESS =====")
    print("Total Attempted:", data["attempted"])
    print("Correct Answers:", data["correct"])

    if data["attempted"] > 0:
        accuracy = data["correct"] / data["attempted"] * 100
        print("Accuracy:", round(accuracy, 1), "%")

    print("Wrong Questions:", len(data["wrong"]))

    print("\nTopic-wise Scores:")
    for topic, score in data["topic_scores"].items():
        print(topic, ":", score)

questions = [
    ("X-ray Basics", "X-rays are which type of waves?",
     ["Sound waves", "Electromagnetic waves", "Water waves"], 1,
     "X-rays are a form of electromagnetic radiation."),

    ("X-ray Basics", "Which unit is commonly used for radiation dose?",
     ["Sievert", "Kilogram", "Meter"], 0,
     "Sievert is used to express radiation dose effects."),

    ("X-ray Basics", "What does ALARA stand for?",
     ["As Low As Reasonably Achievable", "Always Limit All Radiation", "Automatic Level And Radiation Assessment"], 0,
     "ALARA is a radiation protection principle."),

    ("Chest Anatomy", "How many lungs does a normal human have?",
     ["One", "Two", "Three"], 1,
     "Humans normally have right and left lungs."),

    ("Chest Anatomy", "How many lobes are in the right lung?",
     ["Two", "Three", "Four"], 1,
     "The right lung has three lobes."),

    ("Chest Anatomy", "How many lobes are in the left lung?",
     ["Two", "Three", "Four"], 0,
     "The left lung has two lobes."),

    ("Chest Anatomy", "Which muscle separates thorax and abdomen?",
     ["Diaphragm", "Biceps", "Triceps"], 0,
     "The diaphragm separates the thoracic and abdominal cavities."),

    ("Chest Anatomy", "Where is the heart located?",
     ["Thoracic cavity", "Pelvic cavity", "Cranial cavity"], 0,
     "The heart is located in the thoracic cavity."),

    ("Chest Anatomy", "What is the trachea?",
     ["Airway", "Bone", "Muscle"], 0,
     "The trachea is the windpipe."),

    ("Chest Anatomy", "What does the pleura cover?",
     ["Lungs", "Kidneys", "Brain"], 0,
     "The pleura is a membrane associated with the lungs."),

    ("X-ray Views", "What is the full form of PA?",
     ["Posterior-Anterior", "Anterior-Posterior", "Postero-Lateral"], 0,
     "PA means Posterior to Anterior."),

    ("X-ray Views", "What is the full form of AP?",
     ["Anterior-Posterior", "Posterior-Anterior", "Antero-Lateral"], 0,
     "AP means Anterior to Posterior."),

    ("X-ray Views", "A lateral chest view is taken from which direction?",
     ["Side", "Top", "Bottom"], 0,
     "A lateral view shows the chest from the side."),

    ("X-ray Views", "Which view is commonly used for routine erect chest imaging?",
     ["PA", "Skull AP", "Wrist lateral"], 0,
     "PA is a common routine erect chest projection."),

    ("Radiation Safety", "What does the lead apron help reduce?",
     ["Unnecessary radiation exposure", "Sound", "Magnetic field"], 0,
     "Lead shielding can reduce exposure to scattered radiation."),

    ("Radiation Safety", "What is the purpose of collimation?",
     ["Limit the X-ray beam area", "Increase room light", "Measure temperature"], 0,
     "Collimation restricts the beam to the required area."),

    ("Radiation Safety", "Which principle helps avoid unnecessary repeat imaging?",
     ["Good positioning and preparation", "Taking random images", "Ignoring instructions"], 0,
     "Good preparation and positioning help reduce repeat exposures."),

    ("Image Quality", "What does image contrast describe?",
     ["Difference in image brightness", "Patient height", "Room temperature"], 0,
     "Contrast describes differences between light and dark image areas."),

    ("Image Quality", "What can motion cause in an X-ray image?",
     ["Blur", "Extra color", "Sound"], 0,
     "Movement during exposure can produce image blur."),

    ("Image Quality", "What does an image marker identify?",
     ["Side or projection information", "Patient's weight", "Room number"], 0,
     "Markers help identify laterality or projection information.")
]
def run_quiz(revision=False):
    data = load_progress()

    if revision:
        wrong_questions = data.get("wrong", [])
        pool = [q for q in questions if q[1] in wrong_questions]

        if not pool:
            print("\nNo wrong questions to revise!")
            return
    else:
        pool = questions[:]

    random.shuffle(pool)

    score = 0
    wrong_now = []

    for topic, question, options, answer, explanation in pool:
        print("\nTopic:", topic)
        print("Q:", question)

        for i, option in enumerate(options, 1):
            print(str(i) + ".", option)

        choice = input("Answer (1-3, 0=Skip): ").strip()

        if choice == "0":
            continue

        data["attempted"] += 1

        if choice.isdigit() and int(choice) - 1 == answer:
            print("\nCorrect!")
            score += 1
            data["correct"] += 1
        else:
            print("\nIncorrect!")
            print("Correct answer:", options[answer])
            wrong_now.append(question)

        print("Explanation:", explanation)

        topic_data = data["topic_scores"].setdefault(
            topic, {"attempted": 0, "correct": 0}
        )
        topic_data["attempted"] += 1

        if choice.isdigit() and int(choice) - 1 == answer:
            topic_data["correct"] += 1

    data["wrong"] = wrong_now
    save_progress(data)

    print("\n===== QUIZ RESULT =====")
    print("Score:", score, "/", len(pool))
    print("Progress saved!")

def topic_quiz():
    topics = sorted(set(q[0] for q in questions))

    print("\n===== SELECT TOPIC =====")
    for i, topic in enumerate(topics, 1):
        print(str(i) + ".", topic)

    choice = input("Choose topic number: ").strip()

    if not choice.isdigit():
        print("Invalid choice!")
        return

    index = int(choice) - 1

    if index < 0 or index >= len(topics):
        print("Invalid choice!")
        return

    selected_topic = topics[index]
    selected_questions = [
        q for q in questions if q[0] == selected_topic
    ]

    print("\nStarting:", selected_topic)
    run_selected_quiz(selected_questions)


def run_selected_quiz(pool):
    data = load_progress()
    score = 0

    for topic, question, options, answer, explanation in pool:
        print("\n" + question)

        for i, option in enumerate(options, 1):
            print(str(i) + ".", option)

        choice = input("Answer (1-3, 0=Skip): ").strip()

        if choice == "0":
            continue

        data["attempted"] += 1

        topic_data = data["topic_scores"].setdefault(
            topic, {"attempted": 0, "correct": 0}
        )
        topic_data["attempted"] += 1

        if choice.isdigit() and int(choice) - 1 == answer:
            print("Correct!")
            score += 1
            data["correct"] += 1
            topic_data["correct"] += 1
        else:
            print("Correct answer:", options[answer])

        print("Explanation:", explanation)

    save_progress(data)
    print("\nTopic Score:", score, "/", len(pool))


def show_revision():
    data = load_progress()
    wrong = data.get("wrong", [])

    pool = [q for q in questions if q[1] in wrong]

    if not pool:
        print("No wrong questions to revise!")
        return

    run_selected_quiz(pool)


def show_menu():
    while True:
        print("\n===== CHEST XRAY AI V10 =====")
        print("1. Complete MCQ Quiz")
        print("2. Topic-wise Quiz")
        print("3. Wrong Answer Revision")
        print("4. Progress Tracking")
        print("0. Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            run_quiz()
        elif choice == "2":
            topic_quiz()
        elif choice == "3":
            show_revision()
        elif choice == "4":
            show_progress()
        elif choice == "0":
            print("Thank you for learning!")
            break
        else:
            print("Invalid choice!")


show_menu()
