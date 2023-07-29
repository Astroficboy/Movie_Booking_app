Vue.component('edit-theater',{
    delimiters: ["[[", "]]"],
    template:`
    <div class="modal-body">
            <form id="editForm" method="POST">
                <div class="form-group">
                    <label for="name">Theater Name</label>
                    <input type="text" class="form-control" id="name" name="name" value="{{ theater.name }}" required>
                </div>
                <div class="form-group">
                    <label for="address">Address</label>
                    <input type="text" class="form-control" id="address" name="address" value="{{ theater.address }}" required>
                </div>
                <div class="form-group">
                    <label for="capacity">Capacity</label>
                    <input type="number" class="form-control" id="capacity" name="capacity" value="{{ theater.capacity }}" required>
                </div>
                <div class="form-group">
                    <label for="screens">Number of Screens</label>
                    <input type="number" class="form-control" id="screens" name="screens" value="{{ theater.screens }}" required>
                </div>
                <button type="submit" class="btn btn-primary">Save Changes</button>
            </form>
        </div>`
})


console.log("from theater management");
const theater_management = new Vue({
    el: "#theater_management",
});