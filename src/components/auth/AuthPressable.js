import { StyleSheet, Text, Pressable } from 'react-native';
import React from 'react';
import { COLOURS } from '../../styles/Colours';

const AuthPressable = (props) => {
    const { onPressHandler, title } = props;

    return (
        <Pressable
            style={styles.button}
            onPress={onPressHandler}
            android_ripple={{ color: '#FFF' }}>
            <Text style={styles.text}>{title}</Text>
        </Pressable>
    );
};

export default AuthPressable;

const styles = StyleSheet.create({
    button: {
        backgroundColor: COLOURS.secondary,
        marginVertical: 5,
        paddingVertical: 10,
        width: '80%',
        height: 40,
        alignItems: 'center',
        borderRadius: 15,
    },
    text: {
        color: 'white',
        fontFamily: 'roboto',
    },
});
