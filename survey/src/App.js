import withFirebaseAuth from 'react-with-firebase-auth'
import * as firebase from 'firebase/app';
import 'firebase/auth';
import firebaseConfig from './firebaseConfig';
import React from 'react';
// import logo from './logo.svg';
import './App.css';
import Survey from './Survey';
// import { render } from '@testing-library/react';

const firebaseApp = firebase.initializeApp(firebaseConfig);
const providers = {
  githubProvider: new firebase.auth.GithubAuthProvider(),
};





class App extends React.Component {
  
  render() {
    const {
      user,
      signOut,
      signInWithGithub,
    } = this.props;

    return (
      <div className="App">
        <header className="App-header">
          {
              
              user
                ? <p>Hello, {user.displayName} {user.email}</p>
                : <p>Please sign in.</p>
          }

          {
              user
                ? <div><button onClick={signOut}>Sign out</button></div>
                : <button onClick={signInWithGithub}>Sign in with GitHub</button>
          }
          {user &&
            <Survey/>
          }
            
        </header>
      </div>
    );
  }
}

const firebaseAppAuth = firebaseApp.auth();

export default withFirebaseAuth({
  providers,
  firebaseAppAuth,
})(App);
