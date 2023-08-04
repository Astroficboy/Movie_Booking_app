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
                    <label for="screen_no">Screen Number</label>
                    <input class="form-control" id="screen_no" name="screen_no" placeholder="5">
                </div>
                <div class="form-group">
                    <label for="total_seats">Total seats</label>
                    <input class="form-control" id="total_seats" name="total_seats" placeholder="5">
                </div>
                <div class="form-group">
                    <label for="price">Price</label>
                    <input class="form-control" id="price" name="price" placeholder="300">
                </div>
                <div class="form-group">
                    <label for="start_date">Start Date</label>
                    <input type="datetime-local" class="form-control" id="start_date" name="start_date">
                </div>
                <div class="form-group">
                    <label for="end_date">End Date</label>
                    <input type="datetime-local" class="form-control" id="end_date" name="end_date">
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
</div>`
  });


  Vue.component('edit-movie', {
    delimiters:["[[", "]]"],
    template:`
    <div class="modal-body">
            <form id="editForm" method="POST" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="movie_name">Movie Name</label>
                    <input type="text" class="form-control" id="movie_name" name="movie_name" value="{{ movie.name }}">
                </div>
                <div class="form-group">
                    <label for="tags">Tags</label>
                    <input type="text" class="form-control" id="tags" name="tags" value="{{ movie.tags }}">
                </div>
                <div class="form-group">
                    <label for="director">Director</label>
                    <input type="number" class="form-control" id="director" name="director" value="{{ movie.director }}">
                </div>
                <div class="form-group">
                    <label for="price">Price</label>
                    <input type="number" class="form-control" id="price" name="price" value="{{ movie.price }}">
                </div>
                <div class="form-group">
                    <label for="theater_name">Theater Name</label>
                    <input type="number" class="form-control" id="theater_name" name="theater_name" value="{{ movie.theater_name }}>
                </div>
                <div class="form-group">
                    <label for="screen_no">Screen Number</label>
                    <input type="number" class="form-control" id="screen_no" name="screen_no" value="{{ movie.screen_no }}">
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
        </div>`
  })
  
  const movieApp = new Vue({
    el: "#movie_card",
    })