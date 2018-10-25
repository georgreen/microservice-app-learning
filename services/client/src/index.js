import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';

import * as serviceWorker from './serviceWorker';
import UserList from './components/UsersList';
import AddUser from './components/AddUser';


class App extends Component {
    state = {
        users: [],
    };

    getUsers = () => {
        axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
            .then(res => this.setState({users: res.data.data.users}))
            .catch(error => console.log(error));
    }

    componentDidMount() {
        this.getUsers();
    }

    render() {
        return (
            <section className="section">
                <div className="container">
                    <div className="columns">
                        <div className="colum is-one-third">
                            <br />
                            <h1 className="title is-1 is-1">All Users</h1>
                            <hr /><br />
                            <AddUser/>
                            <br/><br/>
                            <UserList users={this.state.users}/>
                        </div>
                    </div>
                </div>
            </section>
        )
    }
}

ReactDOM.render(<App />, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: http://bit.ly/CRA-PWA
serviceWorker.unregister();
