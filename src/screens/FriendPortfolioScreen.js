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

const FriendPortfolioScreen = (props) => {
    const [friends, setFriends] = useState([]);
    const { email } = props;

    useConstructor(() => {
        const docRef = collection(fs, 'Friends', 'Accepted', email);
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let friend = docu.data();
                setFriends((friends) => [...friends, friend]);
            });
        });
    });

    console.log(friends);

    return (
        <View style={globalStyles.container}>
            <View style={styles.portfolioContainer}>
                <Text
                    style={[
                        globalStyles.welcomeText,
                        globalStyles.boldText,
                        styles.addFriendText,
                    ]}>
                    {`Add your friends and follow their portfolios!`}
                </Text>
            </View>
            <StatusBar style="auto" />
        </View>
    );
};

export default FriendPortfolioScreen;

const styles = StyleSheet.create({
    portfolioContainer: {
        flex: 1,
        marginTop: 20,
        backgroundColor: COLOURS.secondary,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    addFriendText: {
        // flex: 1,
    },
    addFriendButton: {
        flex: 1,
    },
});
