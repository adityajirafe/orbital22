import { collection, doc, getDoc, getDocs, setDoc } from 'firebase/firestore';
import { fs } from '../firebase';

const trial = () => {
    const docRef = (fs, 'Friends', 'adi');
    setDoc(docRef, { tom: true }, { merge: true });
};
