import { StyleSheet, Image, View } from 'react-native';
import React from 'react';

const CoinValetIcon = (props) => {
    return (
        <View style={styles.image_container}>
            <Image
                source={require('../../assets/images/coinValet_home.jpeg')}
                style={styles.image}
            />
        </View>
    );
};

export default CoinValetIcon;

const styles = StyleSheet.create({
    image: {
        width: 140,
        height: 140,
        borderRadius: 10,
    },
    image_container: {
        flex: 1,
    },
});
