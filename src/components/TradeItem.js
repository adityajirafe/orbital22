import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';

const TradeItem = (props) => {
    const { item, index } = props;
    return (
        <View style={styles.mainContainer}>
            <View
                style={[
                    styles.rowTop,
                    index % 2 == 0 ? styles.even : styles.odd,
                ]}>
                <Text style={styles.coin}>{item.coin}</Text>
                <Text style={styles.text}>{item.name}</Text>
                <Text style={styles.text}>{item.time}</Text>
            </View>
            <View
                style={[
                    styles.rowBottom,
                    index % 2 == 0 ? styles.even : styles.odd,
                ]}>
                <Text style={styles.text}>Units: {'\n' + item.units}</Text>
                <Text style={styles.text}>Price: {'\n' + item.price}</Text>
                <Text style={[styles.value, styles.green]}>
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
    odd: {
        backgroundColor: COLOURS.lightGrey,
    },
    even: {
        backgroundColor: COLOURS.darkGrey,
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 15,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    value: {
        fontFamily: 'roboto-bold',
        fontSize: 15,
        flex: 1,
        justifyContent: 'space-evenly',
    },
    green: {
        color: COLOURS.green,
    },
});
