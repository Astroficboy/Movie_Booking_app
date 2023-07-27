const movie = Vue.createApp({
    delimiters: ["{[", "]}"],
    compilerOptions: {
        isCustomElement: (tag) => ['add-movie', 'show-movie'].includes(tag)
    }
});

movie.component('show-movie',{
    template:`
    <div class="row">
        <div>
            <div class="col">
                <p></p>
                <div class="card" style="width: 10rem; " :class="{ rate: movie.rating > 4 }">
                    <img :src="movie.img" :alt="movie.title" class="card-img-top">
                    <div class="card-body">
                        <div id="showName"><strong>{[ movie.title ]}</strong></div>
                        <div id="director">Directed by: {[ movie.director ]}</div> 
                        <div id="rating">Rating: {[ movie.rating ]}</div>
                        <div id="price">Price</div>
                        <p></p>
                        <a href="/bookings"><button type="button" class="btn btn-primary">Book Tickets</button></a>
                    </div>
                </div>
            </div>
        </div>
    </div>`
});

movie.component('add-movie',{
    template:`
    <p></p>
    <form class="form-floating", method="POST" enctype="multipart/form-data">
        <div class="row">
        <div class="col"></div>
            <div class="col">
                <label for="show_name">Movie name</label>
                <input class="form-control" id="show_name" name="show_name" placeholder="Oppenheimer">
                <label for="tags">Tags</label>
                <input class="form-control" id="tags" name="tags" placeholder="Baner">
                <label for="director">Director</label>
                <input class="form-control" id="director" name="director" placeholder="300">
                <label for="theater_name">Theater Name</label>
                <input class="form-control" id="theater_name" name="theater_name" placeholder="300">
                <label for="screen_no">Screens</label>
                <input class="form-control" id="screen_no" name="screen_no" placeholder="300">
                <label for="image">Image</label>
                <input type="file" class="form-control" id="image" name="image" placeholder="300">
                <br>
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </div>
    </form>`
})

movie.mount('#movie_card');

