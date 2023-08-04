Vue.component('admin-login', {
    template:`
    <form method="POST" class="container mt-5 p-4 rounded shadow">
    <h3 class="text-center mb-4">Admin Login</h3>
    <div class="row">
        <div class="col-sm-6">
            <div class="form-group">
                <label for="email">Email address</label>  
                <input 
                    type="email"  
                    class="form-control" 
                    id="email" 
                    name="email" 
                    placeholder="Enter email"
                    required
                />
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <label for="password">Password</label>  
                <input 
                    type="password"  
                    class="form-control" 
                    id="password" 
                    name="password" 
                    placeholder="Enter password"
                    required
                />
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-sm-6">
            <button type="submit" class="btn btn-primary btn-block">Login</button>
        </div>
    </div>
</form>`
})

Vue.component('super-login', {
    template:`
    <form method="POST" class="container mt-5 p-4 rounded shadow">
    <h3 class="text-center mb-4">Super Login</h3>
    <div class="row">
        <div class="col-sm-6">
            <div class="form-group">
                <label for="email">Email address</label>  
                <input 
                    type="email"  
                    class="form-control" 
                    id="email" 
                    name="email" 
                    placeholder="Enter email"
                    required
                />
            </div>
        </div>
        <div class="col-sm-6">
            <div class="form-group">
                <label for="password">Password</label>  
                <input 
                    type="password"  
                    class="form-control" 
                    id="password" 
                    name="password" 
                    placeholder="Enter password"
                    required
                />
            </div>
        </div>
    </div>
    <div class="row justify-content-center">
        <div class="col-sm-6">
            <button type="submit" class="btn btn-primary btn-block">Login</button>
        </div>
    </div>
</form>`
})


Vue.component('register-admin', {
    template:`
    <form method="POST">
    <h3 align="center">Admin registration form</h3>
    <div class="row"><p>

    </p></div>
    <div class="row">
        <div class="col"></div>
        <div class="col"></div> 
        <div class="col">
            <div class="form-group">
                <label for="firstName">First Name</label>  
                <input 
                    type="text"  
                    class="form-control" 
                    id="firstName" 
                    name="firstName" 
                    placeholder="Enter first name"
                />
            </div>
        </div>

        <div class="col">
            <div class="form-group">
                <label for="lastName">Last Name</label>  
                <input 
                    type="text"  
                    class="form-control" 
                    id="lastName" 
                    name="lastName" 
                    placeholder="Enter last name"
                />
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="col"></div>
        <div class="col">
            <div class="form-group">
                <label for="email">Email address</label>  
                <input 
                    type="email"  
                    class="form-control" 
                    id="email" 
                    name="email" 
                    placeholder="Enter email"
                />
            </div>

            <div class="form-group">
                <label for="password1">Password</label>  
                <input 
                    type="password"  
                    class="form-control"
                    id="password1" 
                    name="password1" 
                    placeholder="Enter password"
                />
            </div>
            <div class="form-group">
                <label for="password2">Password (Confirm)</label>  
                <input 
                    type="password"  
                    class="form-control" 
                    id="password2" 
                    name="password2" 
                    placeholder="Confirm password"
                />
            </div>
            <br/>
            <button type="submit" class="btn btn-primary">Submit</button>
        </div>
    </div>
</form>`
})



const admin_auth = new Vue({
    el: "#auth",
    })