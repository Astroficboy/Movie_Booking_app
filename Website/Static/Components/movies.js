//DEBUG
console.log("Debug : loaded movies.js");

// MOVIES COMPONENT
const movies = Vue.component("movies",{
    //COMPONENT PROPS
    props:["movies"],
    delimiters:["{[", "]}"],
    data: ["Oppenheimer", "Barbie"],
    template:`
    <div class="card text-center card-custom">
    <div class="card-header">
        {[ movies.visibility ]}
    </div>
    <div class="card-body">
        <h5 class="card-title">{[ movies.name ]}</h5>
        <p class="card-text">{[ movies.description ]}</p>
        <p class="card-text">Rating : {[ movies.rating ]}</p>
        <a href="#" class="btn btn-primary card-button-1" @click="redirectToUrl">Open deck</a>
    </div>
  </div>
    `,
    methods: {
        redirectToUrl() {
            window.location.href = "/bookings";
        }
    }

}).mount("#movies")

