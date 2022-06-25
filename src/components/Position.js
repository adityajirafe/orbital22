import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';
import { StyleSheet, Text, View } from 'react-native';
import { COLOURS } from '../styles/Colours';
import { globalStyles } from '../styles/Styles';

const getPrice = (coin, prices) => {
    let price = 0;
    for (let i = 0; i < prices.length; i++) {
        if (prices[i].coin == coin) {
            price = prices[i].price;
            break;
        }
    }
    return price;
};

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const Position = (props) => {
    const { item, index } = props;
    const [price, setPrice] = useState(0);
    useConstructor(() => {
        // console.log('Rendering screen now');
        // Demo Account contains empty trades while email loads
        const priceRef = collection(fs, 'Prices');
        getDocs(priceRef).then((doc) => {
            doc.forEach((docu) => {
                let priceItem = docu.data();
                if (docu.id == item.coin) {
                    setPrice(priceItem.price);
                }
            });
        });
    });
    // console.log(price);
    return (
        <View style={styles.mainContainer}>
            <View
                style={[
                    styles.rowTop,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                <Text style={styles.header}>{item.coin}</Text>
            </View>
            <View
                style={[
                    styles.rowBottom,
                    index % 2 == 0 ? globalStyles.even : globalStyles.odd,
                ]}>
                <Text style={styles.text}>
                    ${price ? (item.qty * price).toFixed(2) : 0.0}
                </Text>
                <Text style={styles.text}>{item.name.toUpperCase()}</Text>
            </View>
        </View>
    );
};

export default Position;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
        backgroundColor: COLOURS.secondary,
        justifyContent: 'center',
        alignItems: 'center',
    },
    rowTop: {
        flex: 1,
        flexDirection: 'row',
        justifyContent: 'space-evenly',
        alignItems: 'center',
        padding: 10,
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
        padding: 10,
        borderBottomLeftRadius: 20,
        borderBottomRightRadius: 20,
        borderLeftWidth: 2,
        borderBottomWidth: 2,
        borderRightWidth: 2,
    },
    text: {
        fontFamily: 'roboto',
        fontSize: 18,
        flex: 1,
        justifyContent: 'space-evenly',
        textAlign: 'center',
    },
    header: {
        fontFamily: 'roboto-bold',
        fontSize: 21,
        flex: 1,
        justifyContent: 'space-evenly',
        textAlign: 'center',
    },
});
