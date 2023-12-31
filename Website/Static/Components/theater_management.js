Vue.component('edit-theater',{
    delimiters: ["[[", "]]"],
    template:`
    <div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Add Theater</h5>
                    <form method="POST" enctype="multipart/form-data">
                        <div class="mb-3">
                            <label for="name" class="form-label">Theater Name</label>
                            <input type="text" class="form-control" id="name" name="name" placeholder="PVR Cinemas">
                        </div>
                        <div class="mb-3">
                            <label for="address" class="form-label">Address</label>
                            <input type="text" class="form-control" id="address" name="address" placeholder="Baner">
                        </div>
                        <div class="mb-3">
                            <label for="capacity" class="form-label">Capacity</label>
                            <input type="number" class="form-control" id="capacity" name="capacity" placeholder="300">
                        </div>
                        <div class="mb-3">
                            <label for="screens" class="form-label">Screens</label>
                            <input type="number" class="form-control" id="screens" name="screens" placeholder="5">
                        </div>
                        <div class="mb-3">
                            <label for="image" class="form-label">Image</label>
                            <input type="file" class="form-control" id="image" name="image" accept="image/*">
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>`
})


console.log("from theater management");
const theater_management = new Vue({
    el: "#theater_management",
});