<script setup>
  import { ref, onMounted } from 'vue';

  // const fetch = require('node-fetch');
  const quizURL = "http://127.0.0.1:5000/quiz"

  let data
  let quizIndex = ref(0)
  let englishWord  = ref("")
  let spanishWord = ref("")
  let answerOptions = []
  let quizLength = 0
  let selectedAnswer = ref("")
  let message = ref("")


  function setAnswerOptions() {
    // reset to an empty array
    answerOptions = []

    // add the correct answer
    answerOptions.push(data.words[quizIndex.value].spanish)
    
    // add 3 random options that are not the correct answer
    let choice = quizIndex.value
    
    for(let i=0; i < 3; i++){

      // don't add words that are already in the array
      while(answerOptions.includes(data.words[choice].spanish)) {
        choice = Math.floor(Math.random() * data.words.length)
      }

      answerOptions.push(data.words[choice].spanish)
    }

    // scramble the answer options so the correct answer isnt
    // always in the same position
    answerOptions = answerOptions.sort((a, b) => 0.5 - Math.random());
  }

  function isCorrectAnswer(){
    return  selectedAnswer.value == data.words[quizIndex.value].spanish
  }

  function isLastQuestion() {
    return quizIndex.value == quizLength - 1
  }

  function loadNextQuestion(){

    quizIndex.value +=1

    englishWord.value  = data.words[quizIndex.value].english
    spanishWord.value = data.words[quizIndex.value].spanish

    //reset the quiz options
    setAnswerOptions()
    selectedAnswer.value = ""
    message.value = ""

  }

  function completeQuiz() {
    message.value = "Congratulations, you finished the quiz!"
  }

  function submitAnswer(){

      if(isCorrectAnswer()){

        if(isLastQuestion()) {
          completeQuiz()
        } else {
          loadNextQuestion()
        }
   
      } else {
        message.value = "Incorrect, Try Again."
      }

  }

  function initializeQuiz() {
    //POST request options
    const options = {}

    // Fetch the quiz data from the API
    fetch(quizURL, {
      method: 'POST',
      body: JSON.stringify(options),
      headers: { 'Content-Type': 'application/json' }
    }).then(res => res.json())
      .then(json => {
        data = json;
        
        englishWord.value = data.words[quizIndex.value].english;
        spanishWord.value = data.words[quizIndex.value].spanish;
        quizLength = data.words.length;

        setAnswerOptions()

      })
      .catch(err => console.log("Unable to load quiz data: " + err))

  }

  // This is a built-in lifecycle hook from Vue
  onMounted(() => {
    console.log("Quiz mounted");
    initializeQuiz()
  });
 
  

</script>

<template>
  <br>
  MULTIPLE CHOICE QUIZ
  <br><br>
  <div id="multiple-choice-quiz">
    <div class = "progress">{{ quizIndex + 1 }}/{{ quizLength }}</div>
    <div class = "question">
        <span class = "prompt">How do you say </span>
        <span class = "keyword">"{{englishWord}}"</span>
    </div>
    <div class = "options">
        <div v-for="option in answerOptions">
            <input type = "radio" :id = "option" name = "answers" :value = "option" v-model="selectedAnswer">
            <label :for ="option"> {{ option }} </label>
        </div>
    </div>
    <button @click="submitAnswer" type ="button"> Submit </button>
    <div class="message">{{ message }}</div>
  </div>
</template>

<style scoped>

</style>
