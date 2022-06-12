import React from 'react';
import { StyleSheet, Text, View } from 'react-native';

const TradeItem = (props) => {
    const { item, index } = props;
    return (
        <View style={styles.mainContainer}>
            <View
                style={[styles.row, index % 2 == 0 ? styles.even : styles.odd]}>
                <Text style={styles.coin}>{item.coin}</Text>
                <Text style={styles.text}>{item.name}</Text>
                <Text style={styles.text}>{item.time}</Text>
            </View>
            <View
                style={[styles.row, index % 2 == 0 ? styles.even : styles.odd]}>
                <Text style={styles.text}>Units: {'\n' + item.units}</Text>
                <Text style={styles.text}>Price: {'\n' + item.price}</Text>
                <Text style={[styles.text, styles.green]}>
                    Value: {'\n' + item.value}
                </Text>
            </View>
        </View>
    );
};

export default TradeItem;

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
