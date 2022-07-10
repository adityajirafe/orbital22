import { StatusBar } from 'expo-status-bar';
import {
    View,
    Text,
    StyleSheet,
    KeyboardAvoidingView,
    Alert,
    Keyboard,
} from 'react-native';
import React, { useState, useEffect } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { COLOURS } from '../styles/Colours';
import {
    AuthTextInput,
    AuthPressable,
    FeatureImage,
    FriendPortfolioList,
} from '../components';
import { handleFriendRequest } from '../firebase/dbhelper';

const FriendPortfolioScreen = (props) => {
    const [friends, setFriends] = useState([]);
    const [isSending, setIsSending] = useState(false);
    const { email } = props;

    const prepare = async () => {
        const docRef = collection(fs, 'Friends', 'Accepted', email);
        await getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let friend = docu.data();
                setFriends((friends) => [...friends, friend]);
            });
        });
    };

    const wait = (timeout) => {
        return new Promise((resolve) => setTimeout(resolve, timeout));
    };

    const refresh = () => {
        setIsSending(true);
        setFriends([]);
        prepare();
        wait(1000).then(() => setIsSending(false));
    };

    useEffect(() => {
        setIsSending(true);
        prepare();
        setIsSending(false);
    }, []);

    return (
        <View style={globalStyles.container}>
            <View style={styles.portfolioContainer}>
                <Text
                    style={[
                        globalStyles.welcomeText,
                        globalStyles.boldText,
                        styles.addFriendText,
                    ]}>
                    {`View your friend's portfolios!`}
                </Text>
                <FriendPortfolioList friends={friends} />
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
