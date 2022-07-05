import { doc, setDoc, updateDoc, collection, getDoc } from 'firebase/firestore';
import { TRADES } from '../data/trades';
import { fs } from '../firebase';

export const createUser = (username, email) => {
    const usernameRef = doc(fs, 'Directory/', 'Users');
    var newUser = {};
    newUser[username] = email;
    updateDoc(usernameRef, newUser);
    // createTradeTemplate(username);
};

const createTradeTemplate = (username) => {
    const templateRef = doc(
        collection(fs, 'UserPortfolio', username, 'trades')
    );
    setDoc(templateRef, { dummy: 'dummy' });
};

export const addDummyData = (email) => {
    let len = TRADES.length;
    console.log(len);
    for (let i = 0; i < len; i++) {
        const trades = TRADES[i];
        console.log(trades);
        const tradeRef = doc(collection(fs, 'UserPortfolio', email, 'trades'));
        setDoc(tradeRef, trades);
        console.log('added');
    }
};

export const compareTime = (timeA, timeB) => {
    let dateComponentsA = timeA.split(',');
    let datePiecesA = dateComponentsA[0].split('-');
    let timePiecesA = dateComponentsA[1].split(':');

    let formattedTimeA = new Date(
        datePiecesA[0],
        datePiecesA[1] - 1,
        datePiecesA[2],
        timePiecesA[0],
        timePiecesA[1],
        timePiecesA[2]
    );
    let dateComponentsB = timeB.split(',');
    let datePiecesB = dateComponentsB[0].split('-');
    let timePiecesB = dateComponentsB[1].split(':');

    let formattedTimeB = new Date(
        datePiecesB[0],
        datePiecesB[1] - 1,
        datePiecesB[2],
        timePiecesB[0],
        timePiecesB[1],
        timePiecesB[2]
    );
    return formattedTimeB - formattedTimeA;
};

export const handleFriendRequest = (email, friendEmail) => {
    const docRef = doc(fs, 'Friends', email);
    setDoc(docRef, { [friendEmail]: false }, { merge: true });

    const friendRef = doc(fs, 'Friends', friendEmail);
    setDoc(friendRef, { [email]: false }, { merge: true });
};

// getDoc(docRef).then((doc) => {
//     if (doc.exists()) {
//         let persons = doc.data();
//         console.log('Document is: ', doc.data());
//         Object.keys(persons).forEach((username) => {
//             console.log(username);
//             setUsers((users) => [...users, username]);
//         });
//     } else {
//         console.log(doc);
//         console.log('No such document');
//     }
// });
