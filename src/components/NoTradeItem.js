import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

const NoTradeItem = () => {
    return (
        <View style={styles.mainContainer}>
            <Text>No Trades Found</Text>
        </View>
    );
};

export default NoTradeItem;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: 'white',
    },
    row: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        padding: 20,
    },
    coin: {
        fontFamily: 'roboto-bold',
        fontSize: 20,
        flex: 1,
    },
    odd: {
        backgroundColor: '#eeeeee',
    },
    even: {
        backgroundColor: '#afafaf',
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 15,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    green: {
        color: 'green',
    },
});
