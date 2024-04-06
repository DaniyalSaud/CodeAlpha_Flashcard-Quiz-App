import customtkinter as ctk
import random
import pandas as pd

class ctkinterApp(ctk.CTk):

    # __init__ function for class ctkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class cTk
        super().__init__(*args, **kwargs)
        self.geometry('800x600')
        self.title('Flashcard Quiz Application')
        self.resizable(False, False)
        font = ctk.CTkFont(family='Century Gothic', size=20, weight='bold')
        text_font = ctk.CTkFont(family='Century Gothic', size=16)
        ctk.set_appearance_mode('System')
        # creating a container
        container = ctk.CTkFrame(self)
        container.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, ReviewFrame, QuizFrame):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, ReviewFrame, QuizFrame respectively with
            # for loop
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    # to display the current frame passed as
    # parameter
    def show_frame(self, cont, clear_counter=False, quiz_page=False):
        frame = self.frames[cont]
        frame.tkraise()
        if clear_counter:
            make_zero()
            refresh_page(frame)
        if quiz_page:
            make_zero()
            frame.change_question()
            correct_answers_cnt[0] = 0
            frame.score.configure(text=f"Score: {correct_answers_cnt[0]*5}/{(len(flash_cards['Answers'])-1)*5}")
            frame.next_question.configure(text="Next", command=frame.change_question)


# first window frame startpage

class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        font = ctk.CTkFont(family='Century Gothic', size=20, weight='bold')
        text_font = ctk.CTkFont(family='Century Gothic', size=16)
        # label of frame Layout 2
        label = ctk.CTkLabel(self, text="Flashcard Application", font=('Century Gothic', 42, 'bold'))
        label.place(relx=0.5, rely=0.1,anchor=ctk.CENTER)

        self.question_label = ctk.CTkLabel(self, text="Question", font=font)
        self.answer_label = ctk.CTkLabel(self, text='Answer', font=font)
        self.questionEntry = ctk.CTkEntry(self, placeholder_text="Enter Question Here...", font=text_font,
                                          width=500, height=50)
        self.answerEntry = ctk.CTkEntry(self, placeholder_text="Enter Answer Here...", font=text_font,
                                        width=500, height=50)
        self.SaveButton = ctk.CTkButton(self, text="Save", font=font, width=100, height=70,
                                         command=(lambda: add_data_to_dict(self.questionEntry.get(), self.answerEntry.get())))

        self.ReviewButton = ctk.CTkButton(self, text="Review Flashcards", font=font, width=200, height=70,
                                            command=lambda: controller.show_frame(ReviewFrame, clear_counter=True))
        self.ReviewButton.place(relx=0.15, rely=0.8, anchor=ctk.W)
        self.QuizButton = ctk.CTkButton(self, text="Take Quiz", font=font, width=200, height=70,
                                        command=lambda: controller.show_frame(QuizFrame, quiz_page=True))
        self.QuizButton.place(relx=0.60, rely=0.8, anchor=ctk.W)

        self.question_label.place(relx=0.1, rely=0.3, anchor=ctk.W)
        self.answer_label.place(relx=0.1, rely=0.45, anchor=ctk.W)
        self.questionEntry.place(relx=0.25, rely=0.3, anchor=ctk.W)
        self.answerEntry.place(relx=0.25, rely=0.45, anchor=ctk.W)
        self.SaveButton.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        

# second window frame ReviewFrame
class ReviewFrame(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        font = ctk.CTkFont(family='Century Gothic', size=20, weight='bold')
        text_font = ctk.CTkFont(family='Century Gothic', size=16)
        label = ctk.CTkLabel(self, text="Flashcard Application", font=('Century Gothic', 42, 'bold'))
        label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        reviewlabel = ctk.CTkLabel(self, text="Review", font=('Century Gothic', 36, 'bold', 'underline'))
        reviewlabel.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        # button to show frame 2 with text
        # layout2
        self.GoBackButton = ctk.CTkButton(self, text="Go Back", width=120, height=70, font=font,
                             command=lambda: controller.show_frame(StartPage, clear_counter=False))

        self.GoBackButton.place(relx=0.1, rely=0.1,anchor=ctk.CENTER)
        self.quesCount = ctk.CTkLabel(self, text="Total: "+ str(counter[0])+'/'+str(len(flash_cards['Questions'])-1), font=('Century Gothic', 22))
        self.quesCount.place(relx=0.8, rely=0.2, anchor=ctk.CENTER)
        self.nextQuestion = ctk.CTkButton(self, text="Next", width=100, height=70, font=font,
                                          command= self.change_question)
        self.nextQuestion.place(relx=0.4, rely=0.8, anchor=ctk.CENTER)
        self.deleteQuestion = ctk.CTkButton(self, text="Delete", width=100, height=70, font=font,
                                          command= self.delete_question)
        self.deleteQuestion.place(relx=0.6, rely=0.8, anchor=ctk.CENTER)

        self.question_label = ctk.CTkLabel(self, text="Q. " + flash_cards['Questions'][counter[0]] , font=('Century Gothic', 22))
        self.answer_label = ctk.CTkLabel(self, text="Ans. " + flash_cards['Answers'][counter[0]], font=('Century Gothic', 22))
        self.question_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)
        self.answer_label.place(relx=0.5, rely=0.53, anchor=ctk.CENTER)

    def delete_question(self):
        if(counter[0] != 0):
            flash_cards['Questions'].pop(counter[0])
            flash_cards['Answers'].pop(counter[0])
            df = pd.DataFrame(flash_cards)
            df.to_csv('flashcards.csv', index=False)
            counter[0] -= 1
            self.question_label.configure(text="Q. " + flash_cards['Questions'][counter[0]])
            self.answer_label.configure(text="Ans. " + flash_cards['Answers'][counter[0]])
            self.quesCount.configure(text="Total: "+ str(counter[0])+'/'+str(len(flash_cards['Questions'])-1))
    def change_question(self):
        if(counter[0] < len(flash_cards['Questions'])-1):
            counter[0] += 1
        self.question_label.configure(text="Q. " + flash_cards['Questions'][counter[0]])
        self.answer_label.configure(text="Ans. " + flash_cards['Answers'][counter[0]])
        self.quesCount.configure(text="Total: "+ str(counter[0])+'/'+str(len(flash_cards['Questions'])-1))

# third window frame QuizFrame
class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        self.selectedOnce = False
        self.controller = controller
        ctk.CTkFrame.__init__(self, parent)
        font = ctk.CTkFont(family='Century Gothic', size=20, weight='bold')
        text_font = ctk.CTkFont(family='Century Gothic', size=16)


        quiz_options = [str(), str(), str(), str()]
        if (len(flash_cards['Answers'][1:])) >= 4:
            rand_num = random.randint(0,3)
            quiz_options[rand_num] = flash_cards['Answers'][counter[0]]
            for i in range(4):
                if i != rand_num:
                    while True:
                        temp = flash_cards['Answers'][random.randint(1, len(flash_cards['Answers'])-1)]
                        if temp not in quiz_options:
                            quiz_options[i] = temp
                            break

        # label of frame Layout 2
        label = ctk.CTkLabel(self, text="Flashcard Application", font=('Century Gothic', 42, 'bold'))
        label.place(relx=0.5, rely=0.1,anchor=ctk.CENTER)
        quizlabel = ctk.CTkLabel(self, text="Quiz", font=('Century Gothic', 36, 'bold', 'underline'))
        quizlabel.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)
        self.question_label = ctk.CTkLabel(self, text="Question.    " + flash_cards['Questions'][counter[0]+1] , font=font)
        self.quesCount = ctk.CTkLabel(self, text="Total: "+ str(counter[0])+'/'+str(len(flash_cards['Questions'])-1), font=('Century Gothic', 22))
        self.quesCount.place(relx=0.8, rely=0.2, anchor=ctk.CENTER)

        self.quesCount = ctk.CTkLabel(self, text="Total: "+ str(counter[0])+'/'+str(len(flash_cards['Questions'])-1), font=('Century Gothic', 22))
        self.quesCount.place(relx=0.8, rely=0.2, anchor=ctk.CENTER)
        self.question_label.place(relx=0.1, rely=0.3, anchor=ctk.W)

        
        self.next_question = ctk.CTkButton(self, text="Next", font=font, width=100, height=70,
                                           command=self.change_question)
        self.next_question.place(relx=0.8, rely=0.8, anchor=ctk.CENTER)
        self.option1_button = ctk.CTkButton(self, text=quiz_options[0], font=font, width=200, height=70,
                                          command=(lambda :self.check_answer(self.option1_button)))
        
        self.option2_button = ctk.CTkButton(self, text=quiz_options[1], font=font, width=200, height=70,
                                          command=(lambda :self.check_answer(self.option2_button)))
        
        self.option3_button = ctk.CTkButton(self, text=quiz_options[2], font=font, width=200, height=70,
                                          command=(lambda :self.check_answer(self.option3_button)))
        
        self.option4_button = ctk.CTkButton(self, text=quiz_options[3], font=font, width=200, height=70,
                                          command=(lambda :self.check_answer(self.option4_button)))
        #Placing Quiz Options
        self.option1_button.place(relx=0.2, rely=0.5, anchor=ctk.W)
        self.option2_button.place(relx=0.2, rely=0.65, anchor=ctk.W)
        self.option3_button.place(relx=0.55, rely=0.5, anchor=ctk.W)
        self.option4_button.place(relx=0.55, rely=0.65, anchor=ctk.W)

        self.score = ctk.CTkLabel(self, text=f"Score: {correct_answers_cnt[0]*5}/{(len(flash_cards['Answers'])-1)*5}", font=font)

        self.score.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.GoBack = ctk.CTkButton(self, text="Go Back", font=font, width=100, height=70,
                             command=lambda: controller.show_frame(StartPage))

        self.GoBack.place(relx=0.1, rely=0.1,anchor=ctk.CENTER)
    def check_answer(self, button):
        if self.selectedOnce == False:
            self.selectedOnce = True
            if(counter[0] == len(flash_cards['Answers'])-1):
                self.next_question.configure(text='Complete', command=lambda: self.controller.show_frame(StartPage))
            if (len(flash_cards['Answers'][1:])) >= 4:
                if (button.cget('text').lower() == flash_cards['Answers'][counter[0]].lower()):
                    correct_answers_cnt[0] += 1
                    self.score.configure(text=f"Score: {correct_answers_cnt[0]*5}/{(len(flash_cards['Answers'])-1)*5}")
                    button.configure(fg_color='green')
                else:
                    button.configure(fg_color='red')

    def change_question(self):
        if(counter[0] < len(flash_cards['Questions'])-1):
            counter[0] += 1
            self.question_label.configure(text="Q. " + flash_cards['Questions'][counter[0]])
            self.selectedOnce = False

            quiz_options = [str(), str(), str(), str()]
            if (len(flash_cards['Answers'][1:])) >= 4:
                rand_num = random.randint(0,3)
                quiz_options[rand_num] = flash_cards['Answers'][counter[0]]
                for i in range(4):
                    if i != rand_num:
                        while True:
                            temp = flash_cards['Answers'][random.randint(1, len(flash_cards['Answers'])-1)]
                            if temp not in quiz_options:
                                quiz_options[i] = temp
                                break
            else:
                for i in range(4):
                    quiz_options[i] = 'Not Available'
            self.option1_button.configure(text=quiz_options[0], fg_color='blue')
            self.option2_button.configure(text=quiz_options[1], fg_color='blue')
            self.option3_button.configure(text=quiz_options[2], fg_color='blue')
            self.option4_button.configure(text=quiz_options[3], fg_color='blue')
            self.quesCount.configure(text="Total: " + str(counter[0])+'/'+str(len(flash_cards['Questions'])-1))


def make_zero():
    counter[0] = 0  # Reset counter to 0

def add_data_to_dict(question, answer):
    if not question or not answer:
        pass
    else:
        flash_cards['Questions'].append(question)
        flash_cards['Answers'].append(answer)
        df = pd.DataFrame(flash_cards)
        df.to_csv('flashcards.csv', index=False)
    print(flash_cards)

def refresh_page(frame):
    frame.question_label.configure(text="Q. " + flash_cards['Questions'][counter[0]])
    frame.answer_label.configure(text="Ans. " + flash_cards['Answers'][counter[0]])
    frame.quesCount.configure(text="Total: " + str(counter[0])+'/'+str(len(flash_cards['Questions'])-1))


flash_cards = dict()
try:
    data = pd.read_csv('flashcards.csv')
    flash_cards['Questions'] = data['Questions'].tolist()
    flash_cards['Answers'] = data['Answers'].tolist()
except:
    print("No previous data found")

    # Some preloaded questions for the quiz
    flash_cards = {'Questions': ["Questions start here",
                             "Who was the first President of the United States?"
                             , "What is a ball?", "What is the capital of Australia?", "What is the largest ocean in the world?",
                             "What is the currency of Japan?"], 'Answers': ["Answers start here",
                                                                                                    "George Washington",
                                                                                                    "A round object",
                                                                                                    "Canberra",
                                                                                                    "Pacific Ocean",
                                                                                                    "Yen"]}

counter = [0]
correct_answers_cnt = [0]
app = ctkinterApp()
app.mainloop()
