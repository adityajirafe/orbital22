import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import React, { useState, useEffect } from 'react';
import { collection, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { COLOURS } from '../styles/Colours';
import { FriendPortfolioList } from '../components';
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
                <View style={styles.headerContainer}>
                    <Text
                        style={[
                            globalStyles.welcomeText,
                            globalStyles.boldText,
                            styles.addFriendText,
                        ]}>
                        {`View your friend's portfolios!`}
                    </Text>
                    <Pressable
                        title={'Refresh'}
                        disabled={isSending}
                        onPress={refresh}
                        style={styles.refreshButton}>
                        <Icon
                            name="refresh"
                            size={24}
                            style={{
                                color: COLOURS.white,
                                flex: 1,
                                marginTop: 10,
                            }}
                        />
                    </Pressable>
                </View>
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
    headerContainer: {
        flex: 0.08,
        flexDirection: 'row',
    },
    addFriendText: {
        flex: 1,
        fontSize: '18',
    },
    addFriendButton: {
        flex: 1,
    },
    refreshButton: {
        flex: 0.15,
        alignContent: 'center',
        justifyContent: 'center',
        marginTop: -10,
    },
});
