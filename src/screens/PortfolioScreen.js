import { StatusBar } from 'expo-status-bar';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';

import { globalStyles } from '../styles/Styles';

import { DashBoard, PositionList } from '../components';
import { COLOURS } from '../styles/Colours';

const useConstructor = (callBack = () => {}) => {
    const [hasBeenCalled, setHasBeenCalled] = useState(false);
    if (hasBeenCalled) return;
    callBack();
    setHasBeenCalled(true);
};

const PortfolioScreen = (props) => {
    const { email } = props;
    // const [prices, setPrices] = useState([]);
    const [positions, setPositions] = useState([]);
    const [metrics, setMetrics] = useState([]);
    useConstructor(() => {
        // console.log('Rendering screen now');
        // Demo Account contains empty trades while email loads
        // const priceRef = collection(fs, 'Prices/');
        // getDocs(priceRef).then((doc) => {
        //     doc.forEach((docu) => {
        //         // console.log(docu.data());
        //         let price = docu.data();
        //         // console.log('price', price);
        //         setPrices((prices) => [...prices, price]);
        //         // console.log(prices);
        //     });
        // });
        // console.log('prices', prices);
        const reference = email
            ? `UserPortfolio/${email}/`
            : 'UserPortfolio/adi/';
        const docRef = collection(fs, reference, 'positions');
        getDocs(docRef).then((doc) => {
            doc.forEach((docu) => {
                // console.log(docu.data());
                let position = docu.data();
                // console.log('position', position);
                setPositions((positions) => [...positions, position]);
                // console.log(positions);
            });
        });
    });
    return (
        <View style={globalStyles.container}>
            <View style={styles.portfolioContainer}>
                <View style={styles.titleContainer}>
                    <Text style={styles.title}>Current positions</Text>
                </View>
                <View style={styles.positionList}>
                    <PositionList positions={positions} />
                </View>
                <View style={styles.titleContainer}>
                    <Text style={styles.title}>Performance</Text>
                </View>
                <DashBoard email={email} />
            </View>
            <StatusBar style="auto" />
        </View>
    );
};

export default PortfolioScreen;

const styles = StyleSheet.create({
    header: {
        paddingTop: 20,
    },
    portfolioContainer: {
        flex: 1,
        marginTop: 20,
        backgroundColor: COLOURS.secondary,
        borderTopLeftRadius: 30,
        borderTopRightRadius: 30,
        paddingHorizontal: 20,
        paddingVertical: 40,
    },
    positionList: {
        flex: 1,
        paddingBottom: 20,
    },
    titleContainer: {
        backgroundColor: COLOURS.background,
        padding: 15,
        marginBottom: 20,
        borderRadius: 20,
        borderWidth: 2,
    },
    title: {
        fontFamily: 'roboto-bold',
        textAlign: 'center',
        fontSize: 16,
    },
});
