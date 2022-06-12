import { doc, setDoc, updateDoc, collection } from 'firebase/firestore';
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

// export const addDummyData = (email) => {
//     let len = TRADES.length;
//     for (let i = 0; i < len; i++) {
//         const trades = TRADES[i];
//         const tradeRef = doc(collection(fs, 'UserPortfolio', email, 'trades'));
//         setDoc(tradeRef, trades);
//         console.log('added');
//     }
// };
