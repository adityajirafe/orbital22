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
import { AuthTextInput, AuthPressable, FeatureImage } from '../components';
import { handleFriendRequest } from '../firebase/dbhelper';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const FriendReqScreen = (props) => {
    const [requests, setRequests] = useState([]);
    const { email, users } = props;
    const [cache, setCache] = useState([]);
    useConstructor(() => {
        const docRef = collection(fs, 'Friends', 'Requests', email);
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let request = docu.data();
                setRequests((requests) => [...requests, request]);
            });
        });
        const friendRef = collection(fs, 'Friends', 'Accepted', email);
        getDocs(friendRef).then((doc) => {
            doc.forEach((docu) => {
                let friend = docu.data();
                setRequests((requests) => [...requests, friend]);
            });
        });
    });

    const [friend, setFriend] = useState('');

    // console.log(requests);

    const restoreForm = () => {
        setFriend('');
        Keyboard.dismiss();
    };

    const friendRequestSentAlert = () => {
        Alert.alert('Friend Request Sent!');
    };

    const usernameNotFoundAlert = () => {
        Alert.alert('Username does not exist!');
    };

    const sameEmailAlert = () => {
        Alert.alert("Please enter a friend's email");
    };

    const requestAlreadySentAlert = () => {
        Alert.alert('Friend request already sent');
    };

    const addFriendHandler = () => {
        setCache((cache) => [...cache, friend]);
        if (users.find((f) => f == friend)) {
            if (friend == email) {
                sameEmailAlert();
                return;
            }
            if (handleFriendRequest(email, friend, requests, cache) == true) {
                friendRequestSentAlert();
            } else {
                requestAlreadySentAlert();
            }
            restoreForm();
            return;
        } else {
            usernameNotFoundAlert();
            restoreForm();
            return;
        }
    };

    return (
        <KeyboardAvoidingView
            style={{ flex: 1 }}
            behavior={Platform.OS === 'ios' ? 'padding' : null}>
            <View style={globalStyles.container}>
                <FeatureImage />
                <View style={styles.addFriendContainer}>
                    <Text
                        style={[
                            globalStyles.welcomeText,
                            globalStyles.boldText,
                            styles.addFriendText,
                        ]}>
                        {`Add your friends and follow their portfolios!`}
                    </Text>
                    <AuthTextInput
                        value={friend}
                        placeholder="Input your friend's email"
                        textHandler={setFriend}
                        style={styles.addFriendButton}
                    />
                    <AuthPressable
                        onPressHandler={addFriendHandler}
                        title={'Send Request'}
                        style={styles.addFriendButton}
                    />
                </View>
                <StatusBar style="auto" />
            </View>
        </KeyboardAvoidingView>
    );
};

export default FriendReqScreen;

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
});
