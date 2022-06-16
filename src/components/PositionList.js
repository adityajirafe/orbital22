import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';
import { StyleSheet, Text, View, FlatList } from 'react-native';
import { COLOURS } from '../styles/Colours';

import Position from './Position';

const PositionList = (props) => {
    const { positions } = props;

    // const positions = [
    //     { coin: 'BTC', value: '$3300' },
    //     { coin: 'RUNE', value: '$421' },
    //     { coin: 'ETH', value: '$5311' },
    //     { coin: 'DOGE', value: '$75' },
    // ];

    return (
        <View style={styles.mainContainer}>
            <FlatList
                style={styles.positionList}
                data={positions}
                renderItem={({ item, index, prices }) => {
                    return (
                        <Position item={item} index={index} price={prices} />
                    );
                }}
            />
        </View>
    );
};

export default PositionList;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
    },
});
