import { StyleSheet, TextInput } from 'react-native';
import React from 'react';
import { COLOURS } from '../../styles/Colours';

const THEME = '#3F3F3F';

const AuthTextInput = (props) => {
    const { secureTextEntry, keyboardType, placeholder, value, textHandler } =
        props;

    return (
        <TextInput
            style={styles.textInput}
            secureTextEntry={secureTextEntry}
            placeholder={placeholder}
            placeholderTextColor={COLOURS.black}
            keyboardType={keyboardType}
            value={value}
            onChangeText={textHandler}
            selectionColor={THEME}
        />
    );
};

export default AuthTextInput;

const styles = StyleSheet.create({
    textInput: {
        alignSelf: 'center',
        borderWidth: 2,
        borderColor: THEME,
        borderRadius: 15,
        width: '80%',
        height: 50,
        paddingHorizontal: 10,
        marginBottom: 15,
    },
});
