import React, { useState } from 'react';
import { StyleSheet, Text, Pressable } from 'react-native';

import { COLOURS } from '../styles/Colours';

const FriendReqButton = (props) => {
    const { onPressHandler, title } = props;

    return (
        <Pressable
            style={[
                styles.button,
                title == 'Accept' ? styles.accept : styles.decline,
            ]}
            onPress={onPressHandler}
            android_ripple={{ color: '#FFF' }}>
            <Text style={styles.text}>{title}</Text>
        </Pressable>
    );
};

export default FriendReqButton;

const styles = StyleSheet.create({
    button: {
        marginVertical: 5,
        paddingVertical: 10,
        width: '40%',
        height: 40,
        alignItems: 'center',
        borderRadius: 15,
    },
    text: {
        color: COLOURS.white,
        fontFamily: 'roboto',
    },
    accept: {
        backgroundColor: COLOURS.green,
    },
    decline: {
        backgroundColor: COLOURS.red,
    },
    complete: {
        backgroundColor: COLOURS.darkGrey,
    },
    incomplete: {},
});
