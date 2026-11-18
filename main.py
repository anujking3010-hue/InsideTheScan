
import json
import os
import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

QUESTIONS = [
    ("X-ray Basics", "X-rays are which type of waves?",
     ["Sound waves", "Electromagnetic waves", "Water waves"], 1,
     "X-rays are electromagnetic radiation."),
    ("X-ray Basics", "Which unit is commonly used for radiation dose?",
     ["Sievert", "Kilogram", "Meter"], 0,
     "Sievert is used to express radiation dose effects."),
    ("X-ray Basics", "What does ALARA stand for?",
     ["As Low As Reasonably Achievable", "Always Limit All Radiation",
      "Automatic Level And Radiation Assessment"], 0,
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
     "The diaphragm separates thoracic and abdominal cavities."),
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
     "Lead shielding can reduce scattered radiation exposure."),
    ("Radiation Safety", "What is the purpose of collimation?",
     ["Limit the X-ray beam area", "Increase room light", "Measure temperature"], 0,
     "Collimation restricts the beam to the required area."),
    ("Radiation Safety", "Which principle helps avoid unnecessary repeat imaging?",
     ["Good positioning and preparation", "Taking random images",
      "Ignoring instructions"], 0,
     "Good preparation helps reduce repeat exposures."),
    ("Image Quality", "What does image contrast describe?",
     ["Difference in image brightness", "Patient height", "Room temperature"], 0,
     "Contrast describes differences between light and dark areas."),
    ("Image Quality", "What can motion cause in an X-ray image?",
     ["Blur", "Extra color", "Sound"], 0,
     "Movement can produce image blur."),
    ("Image Quality", "What does an image marker identify?",
     ["Side or projection information", "Patient's weight", "Room number"], 0,
     "Markers help identify laterality or projection information.")
]


class ChestXrayApp(App):

    def build(self):
        self.progress_file = os.path.join(
            self.user_data_dir, "progress.json"
        )
        self.load_progress()
        self.root_box = BoxLayout(
            orientation="vertical", padding=15, spacing=10
        )
        self.home()
        return self.root_box

    def load_progress(self):
        try:
            with open(self.progress_file) as f:
                self.data = json.load(f)
        except Exception:
            self.data = {
                "attempted": 0,
                "correct": 0,
                "wrong": []
            }

    def save_progress(self):
        with open(self.progress_file, "w") as f:
            json.dump(self.data, f)

    def show(self, widget):
        self.root_box.clear_widgets()
        self.root_box.add_widget(widget)

    def make_button(self, text, callback):
        b = Button(text=text, size_hint_y=None, height=55)
        b.bind(on_release=callback)
        return b

    def home(self, *args):
        layout = BoxLayout(
            orientation="vertical", padding=15, spacing=12
        )
        layout.add_widget(Label(
            text="[b]INSIDE THE SCAN[/b]\nChest X-ray Learning",
            markup=True, font_size=24
        ))
        layout.add_widget(self.make_button(
            "Complete MCQ Quiz", lambda x: self.start_quiz()
        ))
        layout.add_widget(self.make_button(
            "Topic-wise Quiz", lambda x: self.topic_menu()
        ))
        layout.add_widget(self.make_button(
            "Wrong Answer Revision", lambda x: self.start_quiz(True)
        ))
        layout.add_widget(self.make_button(
            "Progress Tracking", lambda x: self.progress()
        ))
        self.show(layout)

    def topic_menu(self):
        layout = BoxLayout(orientation="vertical", padding=10)
        scroll = ScrollView()
        items = BoxLayout(
            orientation="vertical", spacing=8, size_hint_y=None
        )
        items.bind(minimum_height=items.setter("height"))

        topics = sorted(set(q[0] for q in QUESTIONS))
        for topic in topics:
            items.add_widget(self.make_button(
                topic, lambda x, t=topic: self.start_quiz(topic=t)
            ))

        items.add_widget(self.make_button("Back", self.home))
        scroll.add_widget(items)
        layout.add_widget(scroll)
        self.show(layout)

    def start_quiz(self, revision=False, topic=None):
        if revision:
            wrong = self.data["wrong"]
            self.pool = [q for q in QUESTIONS if q[1] in wrong]
        elif topic:
            self.pool = [q for q in QUESTIONS if q[0] == topic]
        else:
            self.pool = QUESTIONS[:]

        if not self.pool:
            self.result_message("No questions available!")
            return

        random.shuffle(self.pool)
        self.score = 0
        self.index = 0
        self.wrong_now = []
        self.show_question()

    def show_question(self):
        if self.index >= len(self.pool):
            self.data["wrong"] = list(dict.fromkeys(self.wrong_now))
            self.save_progress()
            self.result_message(
                "Quiz Completed!\nScore: "
                + str(self.score) + "/" + str(len(self.pool))
            )
            return

        topic, question, options, answer, explanation = (
            self.pool[self.index]
        )

        layout = BoxLayout(
            orientation="vertical", padding=15, spacing=10
        )
        layout.add_widget(Label(
            text=topic + "\n\n" + question, font_size=20
        ))

        for i, option in enumerate(options):
            layout.add_widget(self.make_button(
                option, lambda x, n=i: self.answer(n)
            ))

        layout.add_widget(self.make_button("Skip", self.skip))
        self.show(layout)

    def answer(self, selected):
        q = self.pool[self.index]
        topic, question, options, correct, explanation = q
        self.data["attempted"] += 1

        if selected == correct:
            self.score += 1
            self.data["correct"] += 1
            self.data["wrong"] = [
                w for w in self.data["wrong"] if w != question
            ]
            message = "Correct!"
        else:
            self.wrong_now.append(question)
            message = "Incorrect!\nCorrect answer: " + options[correct]

        self.save_progress()
        self.feedback(message + "\n\n" + explanation)

    def skip(self, *args):
        self.index += 1
        self.show_question()

    def feedback(self, message):
        layout = BoxLayout(
            orientation="vertical", padding=15, spacing=12
        )
        layout.add_widget(Label(text=message, font_size=18))
        layout.add_widget(self.make_button(
            "Next Question", self.next_question
        ))
        self.show(layout)

    def next_question(self, *args):
        self.index += 1
        self.show_question()

    def result_message(self, message):
        layout = BoxLayout(
            orientation="vertical", padding=15, spacing=12
        )
        layout.add_widget(Label(text=message, font_size=20))
        layout.add_widget(self.make_button("Home", self.home))
        self.show(layout)

    def progress(self, *args):
        attempted = self.data["attempted"]
        correct = self.data["correct"]
        accuracy = round(correct * 100 / attempted, 1) if attempted else 0

        self.result_message(
            f"Attempted: {attempted}\n"
            f"Correct: {correct}\n"
            f"Accuracy: {accuracy}%\n"
            f"Wrong Questions: {len(self.data['wrong'])}"
        )


if __name__ == "__main__":
    ChestXrayApp().run()
