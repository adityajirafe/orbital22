import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';
import { globalStyles } from '../styles/Styles';

const TradeItem = (props) => {
    const { item, index } = props;
    return (
        <View style={styles.mainContainer}>
            <View
                style={[
                    styles.rowTop,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                <Text style={styles.coin}>{item.coin}</Text>
                <Text style={styles.text}>{item.name}</Text>
                <Text style={styles.text}>{item.time}</Text>
            </View>
            <View
                style={[
                    styles.rowBottom,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                <Text style={styles.text}>
                    Units: {'\n' + item.units.toFixed(3)}
                </Text>
                <Text style={styles.text}>
                    Price: {'\n' + item.price.toFixed(3)}
                </Text>
                <Text style={[styles.value, styles.green]}>
                    Value: {'\n' + item.value.toFixed(3)}
                </Text>
                <Text
                    style={[
                        styles.text,
                        item.action == 'CLOSED' ? styles.red : styles.blue,
                    ]}>
                    {item.action}
                </Text>
            </View>
        </View>
    );
};

export default TradeItem;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        marginVertical: 2,
    },
    rowTop: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: 20,
        borderTopLeftRadius: 20,
        borderTopRightRadius: 20,
        borderWidth: 2,
    },
    rowBottom: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: 20,
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        borderWidth: 2,
    },
    coin: {
        fontFamily: 'roboto-bold',
        fontSize: 24,
        flex: 1,
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 14,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    value: {
        fontFamily: 'roboto-bold',
        fontSize: 14,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    green: {
        color: COLOURS.green,
    },
    blue: {
        color: COLOURS.blue,
    },
    red: {
        color: COLOURS.red,
    },
});
