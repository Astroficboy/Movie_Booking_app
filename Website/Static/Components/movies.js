  Vue.component('add-movie', {
    template: `
    <div class="container mt-5 shadow-lg p-4 rounded">
    <h2 class="mb-4">Add Movie</h2>
    <form class="form-floating" method="POST" enctype="multipart/form-data">
        <div class="row">
            <div class="col">
                <div class="form-group">
                    <label for="show_name">Movie Name</label>
                    <input class="form-control" id="show_name" name="show_name" placeholder="Oppenheimer">
                </div>
                <div class="form-group">
                    <label for="tags">Tags</label>
                    <input class="form-control" id="tags" name="tags" placeholder="Drama">
                </div>
                <div class="form-group">
                    <label for="director">Director</label>
                    <input class="form-control" id="director" name="director" placeholder="Christopher Nolan">
                </div>
                <div class="form-group">
                    <label for="theater_name">Theater Name</label>
                    <input class="form-control" id="theater_name" name="theater_name" placeholder="PVR Cinemas">
                </div>
                <div class="form-group">
                    <label for="screen_no">Screen Number</label>
                    <input class="form-control" id="screen_no" name="screen_no" placeholder="5">
                </div>
                <div class="form-group">
                    <label for="price">Price</label>
                    <input class="form-control" id="price" name="price" placeholder="300">
                </div>
                <div class="form-group">
                    <label for="image">Movie Poster</label>
                    <input type="file" class="form-control" id="image" name="image" accept="image/*">
                </div>
                <br>
                <button type="submit" class="btn btn-primary">Submit</button>
            </div>
        </div>
    </form>
</div>


    `
  });
  
  const movieApp = new Vue({
    el: "#movie_card",
    })