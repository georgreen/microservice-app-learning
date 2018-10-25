import React from 'react';

const UsersList = (props) => {
    return props.users.map(user => <h4 key = {user.id}className = "box title is-4"> {user.username} </h4>)
};

export default UsersList;