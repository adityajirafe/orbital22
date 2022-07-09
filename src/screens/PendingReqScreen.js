import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import React, { useState, useEffect } from 'react';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { collection, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { COLOURS } from '../styles/Colours';
import { FriendReqList } from '../components';

const PendingReqScreen = (props) => {
    const [requests, setRequests] = useState([]);
    const [isSending, setIsSending] = useState(false);
    const { email } = props;

    const prepare = async () => {
        const docRef = collection(fs, 'Friends', 'Requests', email);
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let request = docu.data();
                setRequests((requests) => [...requests, request]);
            });
        });
    };

    const wait = (timeout) => {
        return new Promise((resolve) => setTimeout(resolve, timeout));
    };

    const refresh = () => {
        setIsSending(true);
        setRequests([]);
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
            <View style={styles.friendListContainer}>
                <View style={styles.headerContainer}>
                    <View style={styles.titleContainer}>
                        <Text style={styles.title}>Pending Requests</Text>
                    </View>
                    <Pressable
                        title={'Refresh'}
                        disabled={isSending}
                        onPress={refresh}>
                        <Icon
                            name="refresh"
                            size={30}
                            style={{
                                color: COLOURS.white,
                                marginTop: 12,
                                marginLeft: 10,
                            }}
                        />
                    </Pressable>
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
    headerContainer: {
        flexDirection: 'row',
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
        flex: 1,
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
