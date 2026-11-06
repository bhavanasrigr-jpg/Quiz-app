
import 'package:flutter/material.dart';

void main() {
  runApp(const QuizApp());
}

class QuizApp extends StatelessWidget {
  const QuizApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Quiz App',
      theme: ThemeData(
        colorSchemeSeed: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const QuizScreen(),
    );
  }
}

// QUESTION MODEL

class Question {
  final String question;
  final List<String> options;
  final int correctAnswer;

  Question(this.question, this.options, this.correctAnswer);
}

// QUIZ SCREEN

class QuizScreen extends StatefulWidget {
  const QuizScreen({super.key});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  final List<Question> questions = [
    Question('Which language is used for Flutter?',
        ['Java', 'Dart', 'Python', 'C++'], 1),
    Question('Which company developed Flutter?',
        ['Google', 'Microsoft', 'Apple', 'Amazon'], 0),
    Question('What is the entry point of Dart?',
        ['start()', 'main()', 'run()', 'init()'], 1),
    Question('Which widget arranges children vertically?',
        ['Row', 'Stack', 'Column', 'Container'], 2),
    Question('Which widget displays text?',
        ['Text', 'Image', 'Icon', 'Scaffold'], 0),
    Question('Which keyword creates a constant?',
        ['var', 'final', 'const', 'static'], 2),
    Question('Which widget creates a button?',
        ['TextField', 'ElevatedButton', 'Column', 'Padding'], 1),
    Question('Which language is used to style Flutter apps?',
        ['HTML', 'CSS', 'Dart', 'SQL'], 2),
    Question('Which widget provides a scrollable list?',
        ['ListView', 'Center', 'Icon', 'Text'], 0),
    Question('Which method updates StatefulWidget UI?',
        ['build()', 'setState()', 'main()', 'dispose()'], 1),
  ];

  int currentQuestion = 0;
  int score = 0;
  int? selectedAnswer;
  bool answered = false;

  void selectAnswer(int index) {
    if (answered) return;

    setState(() {
      selectedAnswer = index;
      answered = true;

      if (index == questions[currentQuestion].correctAnswer) {
        score++;
      }
    });
  }

  void nextQuestion() {
    if (currentQuestion < questions.length - 1) {
      setState(() {
        currentQuestion++;
        selectedAnswer = null;
        answered = false;
      });
    } else {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            score: score,
            total: questions.length,
            onRestart: restartQuiz,
          ),
        ),
      );
    }
  }

  void restartQuiz() {
    setState(() {
      currentQuestion = 0;
      score = 0;
      selectedAnswer = null;
      answered = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    Question q = questions[currentQuestion];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Flutter Quiz'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),

      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              'Question ${currentQuestion + 1} of ${questions.length}',
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 15),

            LinearProgressIndicator(
              value: (currentQuestion + 1) / questions.length,
              color: Colors.deepPurple,
              minHeight: 8,
            ),

            const SizedBox(height: 35),

            Text(
              q.question,
              style: const TextStyle(
                fontSize: 22,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 25),

            ...List.generate(q.options.length, (index) {
              Color buttonColor = Colors.white;

              if (answered) {
                if (index == q.correctAnswer) {
                  buttonColor = Colors.green.shade100;
                } else if (index == selectedAnswer) {
                  buttonColor = Colors.red.shade100;
                }
              }

              return Container(
                margin: const EdgeInsets.only(bottom: 12),
                child: ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: buttonColor,
                    foregroundColor: Colors.black,
                    padding: const EdgeInsets.all(16),
                    alignment: Alignment.centerLeft,
                    side: const BorderSide(
                      color: Colors.deepPurple,
                    ),
                  ),
                  onPressed: () => selectAnswer(index),
                  child: Text(
                    '${String.fromCharCode(65 + index)}. ${q.options[index]}',
                    style: const TextStyle(fontSize: 16),
                  ),
                ),
              );
            }),

            const SizedBox(height: 10),

            if (answered)
              Text(
                selectedAnswer == q.correctAnswer
                    ? 'Correct Answer! 🎉'
                    : 'Wrong Answer! Correct: ${q.options[q.correctAnswer]}',
                style: TextStyle(
                  fontSize: 17,
                  fontWeight: FontWeight.bold,
                  color: selectedAnswer == q.correctAnswer
                      ? Colors.green
                      : Colors.red,
                ),
              ),

            const Spacer(),

            ElevatedButton(
              onPressed: answered ? nextQuestion : null,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.deepPurple,
                foregroundColor: Colors.white,
                padding: const EdgeInsets.all(16),
              ),
              child: Text(
                currentQuestion == questions.length - 1
                    ? 'Show Results'
                    : 'Next Question',
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// RESULTS SCREEN

class ResultScreen extends StatelessWidget {
  final int score;
  final int total;
  final VoidCallback onRestart;

  const ResultScreen({
    super.key,
    required this.score,
    required this.total,
    required this.onRestart,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Quiz Results'),
        centerTitle: true,
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
      ),

      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(25),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(
                Icons.emoji_events,
                size: 100,
                color: Colors.amber,
              ),

              const SizedBox(height: 20),

              const Text(
                'Quiz Completed!',
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 20),

              Text(
                'Your Score: $score / $total',
                style: const TextStyle(
                  fontSize: 25,
                  color: Colors.deepPurple,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 15),

              Text(
                'Percentage: ${(score / total * 100).toStringAsFixed(0)}%',
                style: const TextStyle(fontSize: 20),
              ),

              const SizedBox(height: 30),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () {
                    onRestart();

                    Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const QuizScreen(),
                      ),
                    );
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.deepPurple,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.all(16),
                  ),
                  child: const Text('Restart Quiz'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
