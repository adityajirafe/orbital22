import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';
import { StyleSheet, Text, View, FlatList } from 'react-native';
import { COLOURS } from '../styles/Colours';

const FriendPortfolioList = (props) => {
    const { friends } = props;

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

export default FriendPortfolioList;

const styles = StyleSheet.create({
    mainContainer: {
        flex: 1,
    },
});
