import React, { useState } from 'react';
import { StyleSheet, Text, View, Alert } from 'react-native';
import { FriendReqButton, PressedFriendReqButton } from '.';
import {
    acceptFriendRequest,
    declineFriendRequest,
} from '../firebase/dbhelper';

import { COLOURS } from '../styles/Colours';
import { globalStyles } from '../styles/Styles';

const FriendReqItem = (props) => {
    const { item, index, email } = props;
    const [accepted, setAccepted] = useState(false);
    const [rejected, setRejected] = useState(false);

    const requestAcceptedAlert = () => {
        Alert.alert('Friend Request Accepted!');
    };

    const requestDeclinedAlert = () => {
        Alert.alert('Friend Request Declined!');
    };

    const acceptHandler = () => {
        if (accepted == false && rejected == false) {
            requestAcceptedAlert();
            setAccepted(true);
            acceptFriendRequest(email, item.email);
        } else {
            return;
        }
    };

    const declineHandler = () => {
        if (accepted == false && rejected == false) {
            requestDeclinedAlert();
            setRejected(true);
            declineFriendRequest(email, item.email);
        } else {
            return;
        }
    };

    const doneHandler = () => {
        return;
    };

    return (
        <View style={styles.mainContainer}>
            <View
                style={[
                    styles.rowTop,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                <Text style={styles.text}>{item.email}</Text>
            </View>
            <View
                style={[
                    styles.rowBottom,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                {accepted == false && rejected == false ? (
                    <FriendReqButton
                        onPressHandler={acceptHandler}
                        title={'Accept'}
                        style={styles.complete}
                    />
                ) : (
                    <PressedFriendReqButton
                        onPressHandler={doneHandler}
                        title={'Accept'}
                        style={styles.complete}
                    />
                )}
                {accepted == false && rejected == false ? (
                    <FriendReqButton
                        onPressHandler={declineHandler}
                        title={'Decline'}
                    />
                ) : (
                    <PressedFriendReqButton
                        onPressHandler={doneHandler}
                        title={'Decline'}
                        style={styles.complete}
                    />
                )}
            </View>
        </View>
    );
};

export default FriendReqItem;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        marginVertical: 2,
    },
    rowTop: {
        flex: 1,
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: 25,
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        borderLeftWidth: 2,
        borderTopWidth: 2,
        borderRightWidth: 2,
    },
    rowBottom: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: 25,
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        borderLeftWidth: 2,
        borderBottomWidth: 2,
        borderRightWidth: 2,
    },
    text: {
        fontFamily: 'roboto-bold',
        fontSize: 20,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    value: {
        fontFamily: 'roboto-bold',
        fontSize: 14,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    complete: {
        backgroundColor: COLOURS.black,
    },
    incomplete: {},
    button: {
        marginVertical: 5,
        paddingVertical: 10,
        width: '40%',
        height: 40,
        alignItems: 'center',
        borderRadius: 15,
    },
    accept: {
        backgroundColor: COLOURS.green,
    },
    decline: {
        backgroundColor: COLOURS.red,
    },
});
