import { StatusBar } from 'expo-status-bar';
import {
    View,
    Text,
    StyleSheet,
    KeyboardAvoidingView,
    Alert,
    Keyboard,
} from 'react-native';
import React, { useState } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { COLOURS } from '../styles/Colours';
import { FriendReqList } from '../components';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const PendingReqScreen = (props) => {
    const [requests, setRequests] = useState([]);
    const { email } = props;

    useConstructor(() => {
        const docRef = collection(fs, 'Friends', 'Requests', email);
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let request = docu.data();
                setRequests((requests) => [...requests, request]);
            });
        });
    });

    return (
        <View style={globalStyles.container}>
            {/* <FeatureImage /> */}
            <View style={styles.friendListContainer}>
                <View style={styles.titleContainer}>
                    <Text style={styles.title}>Pending Requests</Text>
                </View>
                <View style={styles.friendList}>
                    <FriendReqList requests={requests} email={email} />
                </View>
            </View>
            <StatusBar style="auto" />
        </View>
    );
};

export default PendingReqScreen;

const styles = StyleSheet.create({
    addFriendContainer: {
        backgroundColor: COLOURS.background,
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingBottom: 100,
    },
    addFriendText: {
        // flex: 1,
    },
    addFriendButton: {
        flex: 1,
    },
    friendListContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        marginTop: 20,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    titleContainer: {
        backgroundColor: COLOURS.background,
        padding: 15,
        marginBottom: 20,
        borderRadius: 20,
        borderWidth: 2,
    },
    title: {
        fontFamily: 'roboto-bold',
        textAlign: 'center',
        fontSize: 16,
    },
    friendList: {
        flex: 1,
        paddingBottom: 20,
    },
});
