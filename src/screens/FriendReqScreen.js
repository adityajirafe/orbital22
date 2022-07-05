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
import { doc, getDoc } from 'firebase/firestore';
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
    const [users, setUsers] = useState([]);
    useConstructor(() => {
        console.log('Rendering screen now');

        const docRef = doc(fs, 'Directory/Users');
        getDoc(docRef).then((doc) => {
            if (doc.exists()) {
                let persons = doc.data();
                console.log('Document is: ', doc.data());
                Object.keys(persons).forEach((username) => {
                    let userEmail = persons[username];
                    console.log(userEmail);
                    setUsers((users) => [...users, userEmail]);
                });
            } else {
                console.log(doc);
                console.log('No such document');
            }
        });
    });

    const { email } = props;
    const [friend, setFriend] = useState('');

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

    const addFriendHandler = () => {
        if (users.find((f) => f == friend)) {
            if (friend == email) {
                sameEmailAlert();
                return;
            }
            handleFriendRequest(email, friend);
            friendRequestSentAlert();
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
