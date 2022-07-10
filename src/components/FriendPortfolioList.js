import React, { useState } from 'react';
import { collection, doc, getDoc, getDocs } from 'firebase/firestore';
import { fs } from '../firebase';
import { StyleSheet, Text, View, FlatList } from 'react-native';
import { COLOURS } from '../styles/Colours';
import FriendPortfolioCard from './FriendPortfolioCard';

const FriendPortfolioList = (props) => {
    const { friends } = props;

    return (
        <View style={styles.mainContainer}>
            <FlatList
                style={styles.positionList}
                data={friends}
                horizontal={true}
                renderItem={({ item, index }) => {
                    return (
                        // <Position item={item} index={index} price={prices} />
                        <FriendPortfolioCard email={item.email} />
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

        // backgroundColor: 'white',
    },
});
