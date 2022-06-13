import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';
import { globalStyles } from '../styles/Styles';

const NoTradeItem = () => {
    const introMessage =
        'Proceed to the CoinValet Telegram Bot\n to make some trades!';
    return (
        <View style={styles.mainContainer}>
            <Text style={styles.text}>No Trades Found</Text>
            <Text style={styles.paragraph}>{introMessage}</Text>
        </View>
    );
};

export default NoTradeItem;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        color: COLOURS.white,
        fontFamily: 'roboto-bold',
        fontSize: 22,
    },
    paragraph: {
        paddingTop: 40,
        color: COLOURS.white,
        fontFamily: 'roboto',
        textAlign: 'center',
        fontSize: 16,
    },
});
