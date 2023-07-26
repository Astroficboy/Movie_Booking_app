const app = Vue.createApp({
    delimiters: ["{[", "]}"],
    data(){
        return{
            title: "Cinepolis IMAX. Aundh"
        }
    },
    methods: {
        changeTitle(){
            this.title = "Something else"
        }
    }
})

app.mount('#admin_dashboard')