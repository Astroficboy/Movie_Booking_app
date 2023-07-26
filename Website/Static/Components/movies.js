
const app = Vue.createApp({
    delimiters: ["{[", "]}"],
    data(){
        return{
            tickets: 0,
            movies: [
                {title: "Oppenheimer", rating: 4.2, director: "Christopher Nolan", img: "/assets/oppenheimer.jpeg"},
                {title: "Barbie", rating:4.2, director: "Greta Gerwig", img: "/assets/Barbie.jpg"},
                {title: "Interstellar", rating:4, director: "Christopher Nolan", img:""},
                {title: "Batman", rating:3.8, director: "Christopher Nolan", img:""},
                {title: "Tenet", rating:3.8, director: "Christopher Nolan", img:""},
            ]
        }
    }
     
})

app.mount('#movie_card')

