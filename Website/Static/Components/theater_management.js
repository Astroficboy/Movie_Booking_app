const theater_management= Vue.createApp({
    delimiters: ["{[", "]}"],
    compilerOptions: {
        isCustomElement: (tag) => ['add-theater', 'show-theater'].includes(tag)
      }
    })

    theater_management.component('add-theater',{
    template:`
    <p></p>
    <form class="form-floating", method="POST" enctype="multipart/form-data">
        <div class="row">
        <div class="col"></div>
            <div class="col">
                <label for="name">Theater name</label>
                <input class="form-control" id="name" name="name" placeholder="PVR Cinemas">
                <label for="address">Address</label>
                <input class="form-control" id="address" name="address" placeholder="Baner">
                <label for="capacity">Capacity</label>
                <input class="form-control" id="capacity" name="capacity" placeholder="300">
                <label for="screens">Screens</label>
                <input class="form-control" id="screens" name="screens" placeholder="300">
                <label for="image">Image</label>
                <input type="file" class="form-control" id="image" name="image" placeholder="300">
                <br>
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </div>
    </form>`
})

theater_management.component('show-theater',{
    template:`
    <div class="row">
        <div class="col"></div>
        <div class="col">
            <div class="card" style="width: 10rem;">
                <img :src="theater.image" :alt="theater.name" class="card-img-top">
                    <div class="card-body">
                        <div id="showName"><strong>{[ theater.name ]}</strong></div>
                        <div id="director">Directed by: {[ theater.address ]}</div> 
                        <div id="rating">Screens: {[ theater.screens ]}</div>
                        <div id="rating">Capacity: {[ theater.capacity ]}</div>
                        <p></p>
                    </div>
            </div>"
        </div>
    </div>`
})

console.log("from theater management")

theater_management.mount('#theater_management')