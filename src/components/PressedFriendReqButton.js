import React from 'react';
import { StyleSheet, Text, Pressable } from 'react-native';

import { COLOURS } from '../styles/Colours';

const PressedFriendReqButton = (props) => {
    const { onPressHandler, title } = props;

    return (
        <Pressable
            style={[styles.button, styles.pressed]}
            onPress={onPressHandler}
            android_ripple={{ color: '#FFF' }}>
            <Text style={styles.text}>{title}</Text>
        </Pressable>
    );
};

export default PressedFriendReqButton;

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
    pressed: {
        backgroundColor: COLOURS.darkestGray,
    },
});
