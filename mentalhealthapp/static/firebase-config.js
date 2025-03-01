import firebase from "firebase/app";
import "firebase/auth";
import "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyCb7eNC6Whx3hPrUgnJC3maCPz79CTBho4",
    authDomain: "absolon-32950.firebaseapp.com",
    projectId: "absolon-32950",
    // storageBucket: "absolon-32950.firebasestorage.app",
    // messagingSenderId: "506304368798",
    // appId: "1:506304368798:web:b8bf0824a2de16da3eab8f",
    // measurementId: "G-1H8PPSYP2D"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

export const auth = firebase.auth();
export const db = firebase.firestore();
